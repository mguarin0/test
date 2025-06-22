import jax.numpy as jnp
from vector_add_jax import vector_add_primitive

a = jnp.ones(1024, dtype=jnp.float32)
b = jnp.ones(1024, dtype=jnp.float32)

out = vector_add_primitive(a, b)
print(out)

