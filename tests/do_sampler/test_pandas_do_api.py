import pytest
import numpy as np

import dowhy.datasets
import dowhy.api

from sklearn.linear_model import LinearRegression


class TestPandasDoAPI(object):
    @pytest.mark.parametrize(["N", "error_tolerance"],
                             [(10000, 0.1),])
    def test_pandas_api_discrete_cause_continuous_confounder(self, N, error_tolerance):
        data = dowhy.datasets.linear_dataset(beta=10,
                                             num_common_causes=1,
                                             num_instruments=1,
                                             num_samples=N,
                                             treatment_is_binary=False)
        X0 = np.random.normal(size=N)
        v = (np.random.normal(size=N) + X0).astype(int)
        y = data['ate']*v + X0 + np.random.normal()
        data['df']['v'] = v
        data['df']['X0'] = X0
        data['df']['y'] = y
        df = data['df'].copy()

        variable_types = {'v': 'd', 'X0': 'c', 'y': 'c'}
        outcome = 'y'
        cause = 'v'
        common_causes = 'X0'
        method = 'weighting'
        causal_df = df.causal.do(x=cause,
                                 variable_types=variable_types,
                                 outcome=outcome,
                                 method=method,
                                 common_causes=common_causes,
                                 proceed_when_unidentifiable=True)

        ate = (causal_df[causal_df.v == 1].mean() \
              - causal_df[causal_df.v == 0].mean())['y']
        error = np.abs(ate - data['ate'])
        res = True if (error < data['ate'] * error_tolerance) else False
        print("Error in ATE estimate = {0} with tolerance {1}%. Estimated={2},True={3}".format(
            error, error_tolerance * 100, ate, data['ate'])
        )
        assert res

    @pytest.mark.parametrize(["N", "error_tolerance"],
                             [(10000, 0.1),])
    def test_pandas_api_discrete_cause_discrete_confounder(self, N, error_tolerance):
        data = dowhy.datasets.linear_dataset(beta=10,
                                             num_common_causes=1,
                                             num_instruments=1,
                                             num_samples=N,
                                             treatment_is_binary=False)
        X0 = np.random.normal(size=N).astype(int)
        v = (np.random.normal(size=N) + X0).astype(int)
        y = data['ate'] * v + X0 + np.random.normal()
        data['df']['v'] = v
        data['df']['X0'] = X0
        data['df']['y'] = y
        df = data['df'].copy()

        variable_types = {'v': 'd', 'X0': 'd', 'y': 'c'}
        outcome = 'y'
        cause = 'v'
        common_causes = 'X0'
        method = 'weighting'
        causal_df = df.causal.do(x=cause,
                                 variable_types=variable_types,
                                 outcome=outcome,
                                 method=method,
                                 common_causes=common_causes,
                                 proceed_when_unidentifiable=True)

        ate = (causal_df[causal_df.v == 1].mean() \
              - causal_df[causal_df.v == 0].mean())['y']
        print('ate', ate)
        error = np.abs(ate - data['ate'])
        res = True if (error < data['ate'] * error_tolerance) else False
        print("Error in ATE estimate = {0} with tolerance {1}%. Estimated={2},True={3}".format(
            error, error_tolerance * 100, ate, data['ate'])
        )
        assert res

    @pytest.mark.parametrize(["N", "error_tolerance"],
                             [(10000, 0.1),])
    def test_pandas_api_continuous_cause_discrete_confounder(self, N, error_tolerance):
        data = dowhy.datasets.linear_dataset(beta=10,
                                             num_common_causes=1,
                                             num_instruments=1,
                                             num_samples=N,
                                             treatment_is_binary=False)
        X0 = np.random.normal(size=N).astype(int)
        v = np.random.normal(size=N) + X0
        y = data['ate'] * v + X0 + np.random.normal()
        data['df']['v'] = v
        data['df']['X0'] = X0
        data['df']['y'] = y
        df = data['df'].copy()

        variable_types = {'v': 'c', 'X0': 'd', 'y': 'c'}
        outcome = 'y'
        cause = 'v'
        common_causes = 'X0'
        method = 'weighting'
        causal_df = df.causal.do(x=cause,
                                 variable_types=variable_types,
                                 outcome=outcome,
                                 method=method,
                                 common_causes=common_causes,
                                 proceed_when_unidentifiable=True)

        ate = LinearRegression().fit(causal_df[['v']], causal_df['y']).coef_[0]
        print('ate', ate)
        error = np.abs(ate - data['ate'])
        res = True if (error < data['ate'] * error_tolerance) else False
        print("Error in ATE estimate = {0} with tolerance {1}%. Estimated={2},True={3}".format(
            error, error_tolerance * 100, ate, data['ate'])
        )
        assert res

    @pytest.mark.parametrize(["N", "error_tolerance"],
                             [(10000, 0.1),])
    def test_pandas_api_continuous_cause_continuous_confounder(self, N, error_tolerance):
        data = dowhy.datasets.linear_dataset(beta=10,
                                             num_common_causes=1,
                                             num_instruments=1,
                                             num_samples=N,
                                             treatment_is_binary=False)
        X0 = np.random.normal(size=N)
        v = np.random.normal(size=N) + X0
        y = data['ate'] * v + X0 + np.random.normal()
        data['df']['v'] = v
        data['df']['X0'] = X0
        data['df']['y'] = y
        df = data['df'].copy()

        variable_types = {'v': 'c', 'X0': 'c', 'y': 'c'}
        outcome = 'y'
        cause = 'v'
        common_causes = 'X0'
        method = 'weighting'
        causal_df = df.causal.do(x=cause,
                                 variable_types=variable_types,
                                 outcome=outcome,
                                 method=method,
                                 common_causes=common_causes,
                                 proceed_when_unidentifiable=True)

        ate = LinearRegression().fit(causal_df[['v']], causal_df['y']).coef_[0]
        print('ate', ate)
        error = np.abs(ate - data['ate'])
        res = True if (error < data['ate'] * error_tolerance) else False
        print("Error in ATE estimate = {0} with tolerance {1}%. Estimated={2},True={3}".format(
            error, error_tolerance * 100, ate, data['ate'])
        )
        assert res
