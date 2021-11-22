import numpy as np
import pandas as pd

from lingam.utils import (
    print_causal_directions,
    print_dagc,
    make_prior_knowledge,
    remove_effect,
    make_dot,
    predict_adaptive_lasso,
    get_sink_variables,
    get_exo_variables,
    find_all_paths,
)


def test_print_causal_directions():
    cdc = {'from': [0, 1, 2, 3], 'to': [1, 2, 3, 4], 'count': [5, 4, 3, 2]}
    print_causal_directions(cdc, n_sampling=5)
    print_causal_directions(cdc, n_sampling=5, labels=['A', 'B', 'C', 'D', 'E'])


def test_print_dagc():
    dagc = {
        'dag': [
            {'from': [0, 1, 2, 3], 'to': [1, 2, 3, 4]},
            {'from': [0, 1, 2, 3], 'to': [1, 2, 3, 0]},
            {'from': [0, 1, 2, 3], 'to': [1, 2, 3, 4]}
        ],
        'count': [5, 2, 1],
    }
    print_dagc(dagc, n_sampling=5)
    print_dagc(dagc, n_sampling=5, labels=['A', 'B', 'C', 'D', 'E'])

def test_make_prior_knowledge():
    pk = make_prior_knowledge(n_variables=5, exogenous_variables=[0], sink_variables=[1], paths=[[2, 3]], no_paths=[[3, 4]])
    assert pk.shape[0]==5 and pk.shape[1]==5

def test_get_sink_variables():
    am = [
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
    ]
    sv = get_sink_variables(adjacency_matrix=am)
    assert len(sv)==2

def test_get_exo_variables():
    am = [
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0],
    ]
    ev = get_exo_variables(adjacency_matrix=am)
    assert len(ev)==2

def test_remove_effect():
    # causal direction: x0 --> x1 --> x3
    x0 = np.random.uniform(size=1000)
    x1 = 2.0 * x0 + np.random.uniform(size=1000)
    x2 = np.random.uniform(size=1000)
    x3 = 4.0 * x1 + np.random.uniform(size=1000)
    X = pd.DataFrame(np.array([x0, x1, x2, x3]).T, columns=['x0', 'x1', 'x2', 'x3'])

    remove_effect(X, remove_features=[0])

def test_make_dot():
    # default
    am = [
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0],
    ]
    ev = make_dot(am, labels=['x0', 'x1', 'x2', 'x3'])

    # default
    am = [
        [0, 1, 1, 0],
        [0, 0, np.nan, 0],
        [0, np.nan, 0, 0],
        [0, 1, 0, 0],
    ]
    ev = make_dot(am, labels=['x0', 'x1', 'x2', 'x3'])

    # prediction
    ev = make_dot(am, prediction_feature_indices=[1, 2], prediction_coefs=[0.1, 0.1])
    ev = make_dot(am, prediction_feature_indices=[1, 2], prediction_target_label='Target', prediction_line_color='#0000FF')
    ev = make_dot(am, prediction_feature_indices=[1, 2], prediction_feature_importance=[0.5, 0.2])

    # invalid adjacency matrix
    am = [
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    try:
        ev = make_dot(am, labels=['x0', 'x1', 'x2', 'x3'])
    except ValueError:
        pass
    else:
        raise AssertionError

    # invalid label size
    am = [
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0],
    ]
    try:
        ev = make_dot(am, labels=['x0', 'x1', 'x2'])
    except ValueError:
        pass
    else:
        raise AssertionError

    # invalid predict settings
    am = [
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0],
    ]
    try:
        ev = make_dot(am, prediction_feature_indices=[1, 2], prediction_coefs=[0.1])
    except ValueError:
        pass
    else:
        raise AssertionError

    try:
        ev = make_dot(am, prediction_feature_indices=[1, 2], prediction_feature_importance=[0.5])
    except ValueError:
        pass
    else:
        raise AssertionError



def test_predict_adaptive_lasso():
    # causal direction: x0 --> x1 --> x3
    x0 = np.random.uniform(size=1000)
    x1 = 2.0 * x0 + np.random.uniform(size=1000)
    x2 = np.random.uniform(size=1000)
    x3 = 4.0 * x1 + np.random.uniform(size=1000)
    X = pd.DataFrame(np.array([x0, x1, x2, x3]).T, columns=['x0', 'x1', 'x2', 'x3'])

    predict_adaptive_lasso(X.values, predictors=[0, 1, 2], target=3)

def test_find_all_paths():
    dag = [
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
    ]
    find_all_paths(np.array(dag), 1, 0)

    # min_causal_effect
    dag = [
        [0, 2, 1, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
    ]
    find_all_paths(np.array(dag), 1, 0, min_causal_effect=1)

    # Invalid DAG: cycle
    dag = [
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
    ]
    try:
        find_all_paths(np.array(dag), 1, 0)
    except ValueError:
        pass
    else:
        raise AssertionError
