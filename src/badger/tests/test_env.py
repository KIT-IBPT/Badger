import pytest


def test_find_env():
    from badger.factory import list_env, get_env

    assert len(list_env()) == 1

    _, configs = get_env('test')
    assert configs['name'] == 'test'
    assert configs['version'] == '1.0'


def test_get_params():
    from badger.factory import get_env

    _, configs = get_env("test")
    params = configs["params"]

    assert params == {"flag": 0}


def test_set_params():
    from badger.factory import get_env, get_intf

    Interface, _ = get_intf("test")
    intf = Interface()

    # Test pass params only
    Environment, _ = get_env("test")
    env = Environment(flag=1)

    assert env.interface is None
    assert env.flag == 1

    # Test pass interface
    env = Environment(interface=intf)
    assert env.interface
    assert env.flag == 0


def test_list_variables():
    from badger.factory import get_env

    Environment, _ = get_env("test")
    env = Environment()

    variables = {f'x{i}': [-1, 1] for i in range(20)}
    assert env.variables == variables

    assert env.variable_names == list(variables.keys())


def test_list_observables():
    from badger.factory import get_env

    Environment, _ = get_env("test")
    env = Environment()

    assert env.observables == ['f']


def test_get_variables():
    from badger.factory import get_env, get_intf

    Interface, _ = get_intf("test")
    intf = Interface()

    # Without interface
    Environment, _ = get_env("test")
    env = Environment()

    with pytest.raises(Exception) as e:
        env._get_variables(["x1", "x2"])

    assert e.type == AssertionError
    assert "Must provide an interface!" in str(e.value)

    # With interface
    env.interface = intf

    variable_outputs = env._get_variables(["x1", "x2"])
    assert variable_outputs == {"x1": 0, "x2": 0}

    # Test getting variables not defined in env
    variable_outputs = env._get_variables(["x21", "x22"])
    assert variable_outputs == {"x21": 0, "x22": 0}


def test_set_variables():
    from badger.factory import get_env, get_intf
    from badger.errors import BadgerIntfChannelError, BadgerEnvVarError

    Interface, _ = get_intf("test")
    intf = Interface()

    # Without interface
    Environment, _ = get_env("test")
    env = Environment()

    variable_inputs = {"x1": 1, "x2": -1}
    with pytest.raises(Exception) as e:
        env._set_variables(variable_inputs)

    assert e.type == AssertionError
    assert "Must provide an interface!" in str(e.value)

    # With interface
    env.interface = intf

    env._set_variables(variable_inputs)
    variable_outputs = env._get_variables(["x1", "x2"])
    assert variable_outputs == {"x1": 1, "x2": -1}

    # Test setting variables not defined in env
    variable_inputs_undef = {"x21": 1, "x22": -1}
    with pytest.raises(Exception) as e:
        env._set_variables(variable_inputs_undef)

    assert e.type == BadgerIntfChannelError
    assert "not allowed for safety consideration" in str(e.value)

    variable_outputs = env._get_variables(["x21", "x22"])
    assert variable_outputs == {"x21": 0, "x22": 0}

    # Test setting variables out of range
    variable_inputs_out_range = {"x1": 0, "x2": -2}
    with pytest.raises(Exception) as e:
        env._set_variables(variable_inputs_out_range)

    assert e.type == BadgerEnvVarError
    assert "outside its bounds" in str(e.value)

    variable_outputs = env._get_variables(["x1", "x2"])
    assert variable_outputs == {"x1": 1, "x2": -1}  # values shouldn't change


def test_get_observables():
    from badger.factory import get_env, get_intf
    from badger.errors import BadgerEnvObsError

    Interface, _ = get_intf("test")
    intf = Interface()

    # Without interface
    Environment, _ = get_env("test")
    env = Environment()

    with pytest.raises(Exception) as e:
        env._get_observables(["f"])

    assert e.type == AssertionError
    assert "Must provide an interface!" in str(e.value)

    # With interface
    env.interface = intf

    variable_outputs = env._get_observables(["f"])
    assert variable_outputs == {"f": 0}

    variable_inputs = {"x1": 1, "x2": -1}
    env._set_variables(variable_inputs)
    variable_outputs = env._get_observables(["f"])
    assert variable_outputs == {"f": 2}

    # Test getting observables not defined in env
    with pytest.raises(Exception) as e:
        variable_outputs = env._get_observables(["g"])

    assert e.type == BadgerEnvObsError
    assert "not found in environment" in str(e.value)
