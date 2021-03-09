import os

import pandas as pd

from chronix2grid import constants
from chronix2grid import utils
from chronix2grid.generation import generation_utils
from chronix2grid.generation.dispatch import generate_dispatch, EconomicDispatch

class GeneratorBackend:
    def __init__(self):
        self.general_config_manager = constants.GENERAL_CONFIG
        self.load_config_manager = constants.LOAD_GENERATION_CONFIG
        self.res_config_manager = constants.RENEWABLE_GENERATION_CONFIG
        self.loss_config_manager = constants.LOSS_GENERATION_CONFIG
        self.dispatch_config_manager = constants.DISPATCH_GENERATION_CONFIG

        self.consumption_backend_class = constants.LOAD_GENERATION_BACKEND
        self.dispatch_backend_class = constants.DISPATCH_GENERATION_BACKEND
        self.hydro_backend_class = constants.HYDRO_GENERATION_BACKEND
        self.renewable_backend_class = constants.RENEWABLE_GENERATION_BACKEND
        self.loss_backend_class = constants.LOSS_GENERATION_BACKEND

    # Call generation scripts n_scenario times with dedicated random seeds
    def run(self, case, n_scenarios, input_folder, output_folder, scen_names,
            time_params, mode='LRTK', scenario_id=None,
            seed_for_loads=None, seed_for_res=None, seed_for_disp=None):
        """
        Main function for chronics generation. It works with three steps: load generation, renewable generation (solar and wind) and then dispatch computation to get the whole energy mix

        Parameters
        ----------
        case (str): name of case to study (must be a folder within input_folder)
        n_scenarios (int): number of desired scenarios to generate for the same timescale
        input_folder (str): path of folder containing inputs
        output_folder (str): path where outputs will be written (intermediate folder case/year/scenario will be used)
        mode (str): options to launch certain parts of the generation process : L load R renewable T thermal

        Returns
        -------

        """

        utils.check_scenario(n_scenarios, scenario_id)

        print('=====================================================================================================================================')
        print('============================================== CHRONICS GENERATION ==================================================================')
        print('=====================================================================================================================================')

        # in multiprocessing, n_scenarios=1 here
        if n_scenarios >= 2:
            seeds_for_loads, seeds_for_res, seeds_for_disp = generation_utils.generate_seeds(
                n_scenarios, seed_for_loads, seed_for_res, seed_for_disp
            )
        else:
            seeds_for_loads = [seed_for_loads]
            seeds_for_res = [seed_for_res]
            seeds_for_disp = [seed_for_disp]

        # dispatch_input_folder, dispatch_input_folder_case, dispatch_output_folder = gu.make_generation_input_output_directories(input_folder, case, year, output_folder)
        general_config_manager = self.general_config_manager(
            name="Global Generation",
            root_directory=input_folder,
            input_directories=dict(case=case),
            required_input_files=dict(case=['params.json']),
            output_directory=output_folder
        )
        general_config_manager.validate_configuration()
        params = general_config_manager.read_configuration()

        params.update(time_params)
        params = generation_utils.updated_time_parameters_with_timestep(params, params['dt'])

        load_config_manager = self.load_config_manager(
            name="Loads Generation",
            root_directory=input_folder,
            input_directories=dict(case=case, patterns='patterns'),
            required_input_files=dict(case=['loads_charac.csv', 'params_load.json'],
                                      patterns=['load_weekly_pattern.csv']),
            output_directory=output_folder
        )
        load_config_manager.validate_configuration()
        params_load, loads_charac = load_config_manager.read_configuration()
        params_load.update(params)

        res_config_manager = self.res_config_manager(
            name="Renewables Generation",
            root_directory=input_folder,
            input_directories=dict(case=case, patterns='patterns'),
            required_input_files=dict(case=['prods_charac.csv', 'params_res.json'],
                                      patterns=['solar_pattern.npy']),
            output_directory=output_folder
        )
        params_res, prods_charac = res_config_manager.read_configuration()
        params_res.update(params)

        dispath_config_manager = self.dispatch_config_manager(
            name="Dispatch",
            root_directory=input_folder,
            output_directory=output_folder,
            input_directories=dict(params=case),
            required_input_files=dict(params=['params_opf.json'])
        )
        dispath_config_manager.validate_configuration()
        params_opf = dispath_config_manager.read_configuration()
        grid_folder = os.path.join(input_folder, case)
        grid_path = os.path.join(grid_folder, constants.GRID_FILENAME)
        dispatcher = EconomicDispatch.init_dispatcher_from_config(grid_path, input_folder)
        loss = None

        ## Launch proper scenarios generation
        seeds_iterator = zip(seeds_for_loads, seeds_for_res, seeds_for_disp)

        for i, (seed_load, seed_res, seed_disp) in enumerate(seeds_iterator):

            if n_scenarios > 1:
                scenario_name = scen_names(i)
            else:
                scenario_name = scen_names(scenario_id)

            scenario_folder_path = os.path.join(output_folder, scenario_name)

            print("================ Generating " + scenario_name + " ================")
            if 'L' in mode:
                load, load_forecasted = self.do_l(scenario_folder_path, seed_load, params_load, loads_charac, load_config_manager)
            if 'R' in mode:
                prod_solar, prod_solar_forecasted, prod_wind, prod_wind_forecasted = self.do_r(scenario_folder_path, seed_res, params_res,
                                                                                               prods_charac,
                                                                                               res_config_manager)
            if 'D' in mode:
                loss_config_manager = self.loss_config_manager(
                    name="Loss",
                    root_directory=input_folder,
                    output_directory=output_folder,
                    input_directories=dict(params=case),
                    required_input_files=dict(params=['params_loss.json'])
                )

                self.do_d(input_folder, scenario_folder_path,
                                     load, prod_solar, prod_wind,
                                     params, loss_config_manager)
            if 'T' in mode:
                dispatch_results = self.do_t(dispatcher, scenario_name, load, prod_solar, prod_wind,
                                             grid_folder, scenario_folder_path, seed_disp, params, params_opf, loss)
            print('\n')
        return params, loads_charac, prods_charac

    def do_l(self, scenario_folder_path, seed_load, params, loads_charac, load_config_manager):
        generator_loads = self.consumption_backend_class(scenario_folder_path, seed_load, params, loads_charac, load_config_manager,
                                                         write_results=True)
        load, load_forecasted = generator_loads.run()
        return load, load_forecasted

    def do_r(self, scenario_folder_path, seed_res, params, prods_charac, res_config_manager):
        generator_enr = self.renewable_backend_class(scenario_folder_path, seed_res, params,
                                                     prods_charac,
                                                     res_config_manager, write_results=True)

        prod_solar, prod_solar_forecasted, prod_wind, prod_wind_forecasted = generator_enr.run()
        return prod_solar, prod_solar_forecasted, prod_wind, prod_wind_forecasted

    def do_d(self, input_folder, scenario_folder_path,
                                     load, prod_solar, prod_wind,
                                     params, loss_config_manager):

        generator_loss = self.loss_backend_class(input_folder, scenario_folder_path,
                                     load, prod_solar, prod_wind,
                                     params, loss_config_manager)
        loss = generator_loss.run()
        return loss

    def do_t(self, dispatcher, scenario_name, load, prod_solar, prod_wind, grid_folder,
             scenario_folder_path, seed_disp, params, params_opf, loss):
        prods = pd.concat([prod_solar, prod_wind], axis=1)
        res_names = dict(wind=prod_wind.columns, solar=prod_solar.columns)
        dispatcher.chronix_scenario = EconomicDispatch.ChroniXScenario(load, prods, res_names,
                                                                       scenario_name, loss)

        dispatch_results = generate_dispatch.main(dispatcher, scenario_folder_path,
                                                 scenario_folder_path, grid_folder,
                                                  seed_disp, params, params_opf)
        return dispatch_results