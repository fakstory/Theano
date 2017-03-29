from .config import test_ctx_name, mode_with_gpu

from ..type import (get_context, GpuArrayType, GpuArraySharedVariable,
                    gpuarray_shared_constructor)

import pygpu
import numpy as np

from theano.misc.tests.test_may_share_memory import may_share_memory_core
from theano.misc.pkl_utils import dump, load

from theano.tensor.tests.test_opt import test_fusion as t_fusion

class test_fusion(t_fusion):
    mode = mode_with_gpu
    shared = gpuarray_shared_constructor


def test_may_share_memory():
    ctx = get_context(test_ctx_name)
    a = pygpu.empty((5, 4), context=ctx)
    b = pygpu.empty((5, 4), context=ctx)

    may_share_memory_core(a, b)


def test_dump_load():
    x = GpuArraySharedVariable('x',
                               GpuArrayType('float32', (1, 1), name='x',
                                            context_name=test_ctx_name),
                               [[1]], False)

    with open('test', 'wb') as f:
        dump(x, f)

    with open('test', 'rb') as f:
        x = load(f)

    assert x.name == 'x'
    np.testing.assert_allclose(x.get_value(), [[1]])
