# AdvSce

**AdvSce** is a tool capable of generating safety-critical scenarios for testing autonomous driving systems. The tool introduces additional traffic participants that can perturb the behavior of ego vehicles from any existing scenarios within the operational domain of the system under test.

# Usage

Use AdvSce to create and execute a scenario.

```python
from advsce.scenario import ScenarioDescription
from advsce.map import Map

MAP_NAME = 'SanFrancisco'
map_data = Map(MAP_NAME)

scenario = ScenarioDescription(simulator='SVL', map_name=MAP_NAME, dration=60)
ego_vehilce = AgentDescription(
    id='aut', agent_type='EGO', model_name='Lincoln2017MKZ', 
    init_state = map_data.lanes['lane_1'].get_normal_state_by_s(5),
    controller = ApolloController(
        destination=map_data.lanes['lane_1'].get_nromal_state_by_s(-5).position)
)
scenario.add_agent(ego_vehilce)

simulation_result = scenario.exec()
```

Execute perturbation.

```python
generator = HeuristicSearch(
    base_result = simulation_result, 
    max_additional_agent_num = 3, 
    controller_settings = {
        'default': [LaneFollowController(max_speed = 0), 
                    LaneFollowController(max_speed = 5)]
    }
)

for perturbed_result in generator.search():
    ...
```

