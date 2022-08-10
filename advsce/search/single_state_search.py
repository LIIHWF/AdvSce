

from advsce.geometry import check_intersect
from enum import Enum
from inspect import trace
from advsce import scenario
from advsce.controller.controller import ApolloController, LaneFollowController
from advsce.simulator.common import SimulatorType
from advsce.simulator import AgentState, AgentType, SimulatorType
from advsce.map import Map, LaneTurn
from advsce.analyzer import TraceAnalyzer
from advsce.scenario import ScenarioDescription, AgentDescription
import logging

class MutAgentInfo:
    def __init__(self, id, agent_type, agent_model, controller, start_lane, min_s=-float('inf'), max_s=float('inf')):
        self.id = id
        self.agent_type = agent_type
        self.agent_model = agent_model
        self.controller = controller
        self.start_lane = start_lane
        self.min_s = max(min_s, 5)
        self.max_s = min(max_s, start_lane.length - 5)

    def determined(self, delta=0.5):
        return self.min_s >= self.max_s - delta
    
    def get_description(self):
        mid_s = (self.min_s + self.max_s) / 2
        return AgentDescription(self.id, self.agent_type, self.agent_model, self.start_lane.get_normal_state_by_s(mid_s), self.controller)

    def get_upper(self):
        mid_s = (self.min_s + self.max_s) / 2
        return MutAgentInfo(self.id, self.agent_type, self.agent_model, self.controller, self.start_lane, mid_s, self.max_s)

    def get_lower(self):
        mid_s = (self.min_s + self.max_s) / 2
        return MutAgentInfo(self.id, self.agent_type, self.agent_model, self.controller, self.start_lane, self.min_s, mid_s)

class SingleStateSearch:
    def __init__(self, base_scenario, mut_agent_info, expected_lane, time_limit, target_agent_id='aut', reverse=False, delta=0.5, max_iter=float('inf')):
        self.base_scenario = base_scenario
        self.mut_agent_info = mut_agent_info
        self.mut_agent_info = mut_agent_info
        self.expected_lane = expected_lane
        self.time_limit = time_limit
        self.target_agent_id = target_agent_id
        self.reverse = reverse
        self.delta = delta
        self.max_iter = max_iter

    def search(self):
        # on_lane = lambda analyzer, lane, t: (analyzer.lane_info[t].fl.lane == lane or \
        #                                      analyzer.lane_info[t].fr.lane == lane or \
        #                                      analyzer.lane_info[t].fl.lane == lane or \
        #                                      analyzer.lane_info[t].fl.lane == lane) and \
        #                                      not lane.get_sl_by_xy(analyzer.trace[t].position) is None

        on_lane = lambda analyzer, lane, t: not lane.get_sl_by_xy(analyzer.trace[t].position) is None and \
                                            lane.get_sl_by_xy(analyzer.trace[t].position).d < 1

        mut_agent_info = self.mut_agent_info
        cnt = 0
        while not mut_agent_info.determined(self.delta) and cnt < self.max_iter:
            cnt += 1
            logging.info(f'current range {mut_agent_info.min_s} {mut_agent_info.max_s} \ntesting on {(mut_agent_info.min_s + mut_agent_info.max_s) / 2} \n')
            scenario = self.base_scenario.copy()
            scenario.add_agent(mut_agent_info.get_description())
            if not scenario.available:
                break
            scenario.time_step = 0.5
            result = scenario.exec()
            mut_analyzer = TraceAnalyzer(result.traces[mut_agent_info.id], scenario.map)
            tar_analyzer = TraceAnalyzer(result.traces[self.target_agent_id], scenario.map)

            ticks = result.aut_analyzer.lane_info.ticks
            ticks_length = len(ticks)
            i = 0
            while i < ticks_length and \
                  not on_lane(mut_analyzer, self.expected_lane, ticks[i]) and \
                  not on_lane(tar_analyzer, self.expected_lane, ticks[i]):
                i += 1
            
            if i == ticks_length:
                logging.warning('Neither the target agent nor the mutable agent reached the expected lane.')
                break
            
            while i < ticks_length and \
                  on_lane(mut_analyzer, self.expected_lane, ticks[i]) ^ \
                  on_lane(tar_analyzer, self.expected_lane, ticks[i]):
                i += 1

            if i == ticks_length:
                if on_lane(mut_analyzer, self.expected_lane, ticks[i-1]):
                    if self.reverse:
                        mut_agent_info = mut_agent_info.get_upper()
                    else:
                        mut_agent_info = mut_agent_info.get_lower()
                else:
                    if self.reverse:
                        mut_agent_info = mut_agent_info.get_lower()
                    else:
                        mut_agent_info = mut_agent_info.get_upper()
                    
            else:
                while i < ticks_length and \
                      on_lane(mut_analyzer, self.expected_lane, ticks[i]) and \
                      on_lane(tar_analyzer, self.expected_lane, ticks[i]):
                    i += 1
                
                mut_final_sl = self.expected_lane.get_sl_by_xy(mut_analyzer.trace[ticks[i-1]].position, check_bound = False)
                tar_final_sl = self.expected_lane.get_sl_by_xy(tar_analyzer.trace[ticks[i-1]].position, check_bound = False)

                if mut_final_sl.s > tar_final_sl.s:
                    if self.reverse:
                        mut_agent_info = mut_agent_info.get_upper()
                    else:
                        mut_agent_info = mut_agent_info.get_lower()
                else:
                    if self.reverse:
                        mut_agent_info = mut_agent_info.get_lower()
                    else:
                        mut_agent_info = mut_agent_info.get_upper()
                        
            yield result
            
