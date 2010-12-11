import nose

from garlicsim.general_misc import import_tools

from garlicsim.general_misc.address_tools import (describe,
                                                  resolve)


prefix = __name__ + '.'    


#def test_locally_defined_class():
    
    ###########################################################################
    # Testing for locally defined class:
    
    # Currently these tests are commented out, because `describe` doesn't
    # support nested classes yet.
    
    #result = describe(A.B)
    #assert result == prefix + 'A.B'
    #assert resolve(result) is A.B
    
    #result = describe(A.C.D.deeper_method)
    #assert result == prefix + 'A.C.D.deeper_method'
    #assert resolve(result) == A.C.D.deeper_method
    
    #result = describe(A.C.D.deeper_method, root=A.C)
    #assert result == 'C.D.deeper_method'
    #assert resolve(result, root=A.C) == A.C.D.deeper_method
    
    #result = describe(A.C.D.deeper_method, root='A.C.D')
    #assert result == 'D.deeper_method'
    #assert resolve(result, root='A.C.D') == A.C.D.deeper_method
    
    
def test_stdlib():
    
    import email.encoders
    result = describe(email.encoders)
    assert result == 'email.encoders'
    assert resolve(result) is email.encoders
    
    result = describe(email.encoders, root=email.encoders)
    assert result == 'encoders'
    assert resolve(result, root=email.encoders) is email.encoders
    
    result = describe(email.encoders, namespace=email)
    assert result == 'encoders'
    assert resolve(result, namespace=email) is email.encoders
    
    result = describe(email.encoders, root=email.encoders, namespace=email)
    assert result == 'encoders'
    assert resolve(result, root=email.encoders, namespace=email) is \
           email.encoders
    
    
def test_garlicsim():
    
    import garlicsim
    result = describe(garlicsim.data_structures.state.State)
    assert result == 'garlicsim.data_structures.state.State'
    assert resolve(result) is garlicsim.data_structures.state.State
    
    result = describe(garlicsim.data_structures.state.State, shorten=True)
    assert result == 'garlicsim.data_structures.State'
    assert resolve(result) is garlicsim.data_structures.state.State
    
    result = describe(garlicsim.Project, shorten=True)
    assert result == 'garlicsim.Project'
    assert resolve(result) is garlicsim.Project
    
    # When a root or namespace is given, it's top priority to use it, even if it
    # prevents shorterning and results in an overall longer address:
    result = describe(garlicsim.Project, shorten=True,
                         root=garlicsim.asynchronous_crunching)
    assert result == 'asynchronous_crunching.Project'
    assert resolve(result, root=garlicsim.asynchronous_crunching) is \
           garlicsim.Project
    
    result = describe(garlicsim.Project, shorten=True,
                         namespace=garlicsim)
    assert result == 'Project'
    assert resolve(result, namespace=garlicsim) is garlicsim.Project
    
    result = describe(garlicsim.Project, shorten=True,
                         namespace=garlicsim.__dict__)
    assert result == 'Project'
    assert resolve(result, namespace=garlicsim.__dict__) is \
           garlicsim.Project
    
    result = describe(garlicsim.Project, shorten=True,
                         namespace='garlicsim')
    assert result == 'Project'
    assert resolve(result, namespace='garlicsim') is garlicsim.Project
    
    result = describe(garlicsim.Project, shorten=True,
                         namespace='garlicsim.__dict__')
    assert result == 'Project'
    assert resolve(result, namespace='garlicsim.__dict__') is \
           garlicsim.Project
    
    result = describe(garlicsim.data_structures.state.State, root=garlicsim)
    assert result == 'garlicsim.data_structures.state.State'
    assert resolve(result, root=garlicsim) is \
           garlicsim.data_structures.state.State
    
    
    import garlicsim_lib.simpacks.life
    
    result = describe(garlicsim_lib.simpacks.life.state.State.step)
    assert result == 'garlicsim_lib.simpacks.life.state.State.step'
    
    result = describe(garlicsim_lib.simpacks.life.state.State.step,
                      shorten=True)
    assert result == 'garlicsim_lib.simpacks.life.State.step'
    
    result = describe(garlicsim_lib.simpacks.life.state.State.step,
                         root=garlicsim_lib.simpacks.life)
    assert result == 'life.state.State.step'
    
    result = describe(garlicsim_lib.simpacks.life.state.State.step,
                         namespace=garlicsim_lib.simpacks)
    assert result == 'life.state.State.step'
    
    result = describe(garlicsim_lib.simpacks.life.state.State.step,
                         root=garlicsim_lib.simpacks.life, shorten=True)
    assert result == 'life.State.step'
    
    
def test_local_modules():
    
    import garlicsim
    
    from .sample_module_tree import w
    
    z = resolve('w.x.y.z', root=w)

    result = describe(z, root=w)
    assert result == 'w.x.y.z'
    
    result = describe(z, shorten=True, root=w)
    assert result == 'w.y.z'
    
    result = describe(z, shorten=True, root=w)
    assert result == 'w.y.z'
    
    result = describe(z, shorten=True, root=w, namespace='email')
    assert result == 'w.y.z'
    
    result = describe(z, shorten=True, root=garlicsim, namespace=w)
    assert result == 'y.z'
    
    result = describe(z, shorten=True, root=w.x)
    assert result == 'x.y.z'
    
    
def test_ignore_confusing_namespace():
    
    import email.encoders
    import marshal
    
    result = describe(
        email,
        shorten=True,
        namespace={'e': email}
    )
    assert result == 'email'
    
    result = describe(
        email.encoders,
        namespace={'e': email, 'email': email}
    )
    assert result == 'email.encoders'
    
    result = describe(
        email.encoders,
        root=marshal,
        namespace={'e': email, 'email': email}
    )
    assert result == 'email.encoders'
    
    
    
def test_address_in_expression():
    
    import email.encoders
    import marshal
    
    assert describe([object, email.encoders, marshal]) == \
           '[object, email.encoders, marshal]'
    
    assert describe([email.encoders, 7, (1, 3), marshal]) == \
           '[email.encoders, 7, (1, 3), marshal]'
    

def test_specific_objects():
    if not import_tools.exists('multiprocessing'):
        raise nose.SkipTest('`multiprocessing` not installed')
    import multiprocessing
    lock = multiprocessing.Lock()
    describe(lock)
    
    
def test_bad_module_name():
    
    import email

    non_sensical_module_name = '__whoop_dee_doo___rrrar'
    
    my_locals = locals().copy()
    my_locals['__name__'] = non_sensical_module_name
    
    exec 'def f(): pass' in my_locals
    exec ('class A(object):\n'
          '    def m(self): pass') in my_locals
    
    f, A = my_locals['f'], my_locals['A']
    
    assert describe(f) == \
        '.'.join((non_sensical_module_name, 'f'))
    assert describe(f, shorten=True, root=email, namespace={}) == \
        '.'.join((non_sensical_module_name, 'f'))
    
    assert describe(A) == \
        '.'.join((non_sensical_module_name, 'A'))
    assert describe(A, shorten=True, root=email, namespace={}) == \
        '.'.join((non_sensical_module_name, 'A'))
    
    assert describe(A.m) == \
        '.'.join((non_sensical_module_name, 'A.m'))
    assert describe(A.m, shorten=True, root=email, namespace={}) == \
        '.'.join((non_sensical_module_name, 'A.m'))