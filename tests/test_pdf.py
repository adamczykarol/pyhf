import pyhf
import pyhf.simplemodels
import numpy as np
import json

def test_interpcode_0():
    f = pyhf._hfinterp_code0(at_minus_one = 0.5, at_zero =1, at_plus_one = 2.0)
    assert 1+f(-2) == 0.0
    assert 1+f(-1) == 0.5
    assert 1+f(0) == 1.0
    assert 1+f(1) == 2.0
    assert 1+f(2) == 3.0 #extrapolation

    #broadcasting
    assert [1 + x for x in f([-2,-1,0,1,2])] == [0,0.5,1.0,2.0,3.0]

def test_interpcode_1():
    f = pyhf._hfinterp_code1(at_minus_one = 0.9, at_zero =1, at_plus_one = 1.1)

    assert f(-2) == 0.9**2
    assert f(-1) == 0.9
    assert f(0) == 1.0
    assert f(1) == 1.1
    assert f(2) == 1.1**2

    assert np.all(f([-2,-1,0,1,2]) == [0.9**2, 0.9, 1.0, 1.1, 1.1**2])

def test_numpy_pdf_inputs():
    source = {
      "binning": [2,-0.5,1.5],
      "bindata": {
        "data":    [55.0],
        "bkg":     [50.0],
        "bkgerr":  [7.0],
        "sig":     [10.0]
      }
    }
    pdf  = pyhf.simplemodels.hepdata_like(source['bindata']['sig'], source['bindata']['bkg'], source['bindata']['bkgerr'])

    pars = pdf.config.suggested_init()
    data = source['bindata']['data'] + pdf.auxdata


    np_data       = np.array(data)
    np_parameters = np.array(pars)

    assert len(data) == np_data.shape[0]
    assert len(pars) == np_parameters.shape[0]
    assert pdf.logpdf(pars,data) == pdf.logpdf(np_parameters,np_data)
    assert np.array(pdf.logpdf(np_parameters,np_data)).shape == ()


def test_core_pdf_broadcasting():
    data    = [10,11,12,13,14,15]
    lambdas = [15,14,13,12,11,10]
    naive_python = [pyhf._poisson_impl(d, lam) for d,lam in zip(data, lambdas)]

    broadcasted  = pyhf._poisson_impl(data, lambdas)

    assert np.array(data).shape == np.array(lambdas).shape
    assert broadcasted.shape    == np.array(data).shape
    assert np.all(naive_python  == broadcasted)


    data    = [10,11,12,13,14,15]
    mus     = [15,14,13,12,11,10]
    sigmas  = [1,2,3,4,5,6]
    naive_python = [pyhf._gaussian_impl(d, mu,sig) for d,mu,sig in zip(data, mus, sigmas)]

    broadcasted  = pyhf._gaussian_impl(data, mus, sigmas)

    assert np.array(data).shape == np.array(mus).shape
    assert np.array(data).shape == np.array(sigmas).shape
    assert broadcasted.shape    == np.array(data).shape
    assert np.all(naive_python  == broadcasted)