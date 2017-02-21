import pytest
import ufl
from ufl.algorithms.apply_derivatives import apply_derivatives
from ufl.algorithms.apply_algebra_lowering import apply_algebra_lowering

from dolfin_dg.dg_form import homogeneity_tensor, hyper_tensor_product

cells = [ufl.interval, ufl.triangle, ufl.tetrahedron]
families = ["CG", "DG"]
poly_os = [1, 2]

scalar_eles = [ufl.FiniteElement(family, cell, p)
               for family in families
               for cell in cells
               for p in poly_os]

vector_eles = [ufl.VectorElement(family, cell, p, dim=4)
               for family in families
               for cell in cells
               for p in poly_os]

@pytest.fixture
def F1():
    def F_v(u, grad_u):
        return grad_u
    return F_v


@pytest.mark.parametrize("element", scalar_eles)
def test_linear_homogeneity_tensor(element, F1):
    cell_dim = element.cell().geometric_dimension()

    u = ufl.Coefficient(element)
    G = homogeneity_tensor(F1, u)
    G = apply_derivatives(G)

    assert G == ufl.Identity(cell_dim)


@pytest.mark.parametrize("element", scalar_eles)
def test_linear_homogeneity_tensor_product(element, F1):
    cell_dim = element.cell().geometric_dimension()

    u = ufl.Coefficient(element)
    G = homogeneity_tensor(F1, u)
    F = hyper_tensor_product(G, ufl.grad(u))
    F = apply_derivatives(F)

    grad_u = ufl.dot(ufl.Identity(cell_dim), ufl.grad(u))
    expected = ufl.as_matrix([[grad_u[d] for d in range(cell_dim)]])

    assert F == expected


@pytest.mark.parametrize("element", vector_eles)
def test_linear_homogeneity_tensor_product(element, F1):
    cell_dim = element.cell().geometric_dimension()

    u = ufl.Coefficient(element)
    G = homogeneity_tensor(F1, u)
    F = hyper_tensor_product(G, ufl.grad(u))
    F = apply_derivatives(F)

    grad_u = ufl.dot(ufl.Identity(cell_dim), ufl.grad(u))
    expected = ufl.as_matrix([[grad_u[d] for d in range(cell_dim)]])

    assert F == expected

if __name__ == "__main__":
    element = ufl.VectorElement("CG", ufl.triangle, 1, dim=4)
    cell_dim = element.cell().geometric_dimension()

    u = ufl.Coefficient(element)
    G = homogeneity_tensor(F1(), u)
    F = hyper_tensor_product(G, ufl.grad(u))
    F = apply_derivatives(F)

    print F
    # grad_u = ufl.dot(ufl.Identity(cell_dim), ufl.grad(u))

    # print grad_u
    quit()
    expected = ufl.as_matrix([[grad_u[d] for d in range(cell_dim)]])

    assert F == expected