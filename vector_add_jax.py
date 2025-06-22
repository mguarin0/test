# vector_add_jax.py
import jax
import jax.numpy as jnp
from jaxlib import xla_client
import vector_add  # The compiled pybind11 module

ffi = xla_client._xla.ffi
my_custom_call = xla_client.ops.CustomCall

def vector_add_primitive(a, b):
    size = a.size
    out_shape = a.shape

    def impl(a, b):
        return my_custom_call(
            call_target_name="my.vector_add",
            out_shape=xla_client.Shape.array_shape(jnp.dtype('float32'), out_shape),
            operands=(a, b),
            operand_shapes_with_layout=(a.shape, b.shape),
            opaque=bytes([size]),  # Optionally encode metadata
            api_version=1
        )

    return jax.core.Primitive("vector_add").bind(a, b, impl=impl)

# Register JAX translation
jax.interpreters.xla.register_translation(
    vector_add_primitive,
    lambda c, a, b, *, impl: impl(a, b)
)

