import marimo

__generated_with = "0.20.2"
app = marimo.App()

with app.setup:
    # Import modules

    import marimo as mo
    import math
    import numpy as np
    import matplotlib.pyplot as plt

    # Not really needed, but nicer plots
    import seaborn as sns
    sns.set()
    sns.set_context("talk")

    # Define human-readable names for a few constants
    onethird = 1 / 3
    onehalf = 1 / 2
    twothird = 2 / 3
    threefourth = 3 / 4


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # 4th-year course
    ## Lecture 1: Nuclear masses
    ### York, UK, 2025, Tuesday 11 February 2025 11:00-12:00

    Check in code 293110

    jacek.dobaczewski@york.ac.uk
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.image(src="Checkin.250211.png", alt="checkin QR code")
    return


@app.cell(hide_code=True)
def _():
    mo.image(src="Feedback_Directed learning.JD.png", alt="feedback directed learning")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## This course will be delivered in the [Marimo](https://marimo.io) notebook format

    This notebook and all files referred to and linked to, along with its PDF transcript, are available on VLE.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Experimental nuclear masses

    $$M(A,Z) = Z (m_P + m_e) + (A-Z) m_N - E_{atomic} (A,Z) - E_B(A,Z)$$

    $M(A,Z)$ is the mass of the neutral atom

    $Z$ is the atomic number

    $A$ is the mass number; the number of neutrons is thus $N=A-Z$

    $m_P$ is the mass of a proton, $m_e$ is the mass of an electron, $m_N$ is the mass of a neutron

    $E_{atomic} (A,Z)$ is the binding energy of all electrons in the neutral atom

    $E_B(A,Z)$ is the nuclear binding energy

    $E=mc^2$, and $c=1$

    We express all energies and masses in mega-electronovolts (MeV), or eV, keV, or meV.

    1 MeV is the energy that an elementary charge $e$ gains in en electrostatic potential of one million volts
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # The Segré chart ([Table of Nuclides](https://atom.kaeri.re.kr/nuchart/))

    J.Erler et al., [Nature 486, 509 (2012)](https://www.nature.com/articles/nature11188)
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.image(src="Segre.chart.png", alt="Segre chart")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Download the experimental mass table

    [The 2020 Atomic Mass Evaluation](https://www-nds.iaea.org/amdc/ame2020/massround.mas20.txt)
    """)
    return


@app.cell
def _():
    mo.image("AME2016.png", alt="Atomic Mass Evaluation data")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    In Python-friendly format
    """)
    return


@app.cell
def _():
    mo.image("mass16round-sum.png", alt="atomic masses in columnar format")
    return


@app.cell
def _():
    # These variables' names do _not_ start with an underscore '_', so they will be
    # available in other cells in this notebook.
    AME2016k = []
    AME2016N = []
    AME2016Z = []
    AME2016A = []
    AME2016B = []

    # Use NumPy (np) to load the data, then extract values from each row.
    # Note that we use `_i` as a loop variable instead of just `i` because
    # we want to be able to use the same variable in other cells.
    mydata = np.loadtxt('mass16round-sum.txt')
    for _i in range(0, len(mydata)):
        AME2016k.append(mydata[_i][0])  # Remember, Python starts counting at 0
        AME2016N.append(mydata[_i][1])
        AME2016Z.append(mydata[_i][2])
        AME2016A.append(mydata[_i][3])
        AME2016B.append(mydata[_i][4])

    # By default, Marimo shows the value of the last expression in a cell, so we don't
    # need an explicit call to print().
    len(mydata)
    return AME2016A, AME2016B, AME2016N, AME2016Z, mydata


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Current inventory of measured nuclear binding energies contains 2453 entries
    """)
    return


@app.cell
def _(AME2016A, AME2016B):
    # Plot binding energy against mass number.
    plt.plot(AME2016A, AME2016B, 'r.')
    plt.axis([-20, 270, -200, 2000])
    plt.xlabel('Mass number A')
    plt.ylabel('Binding energy (MeV)')
    plt.show()
    return


@app.cell
def _(AME2016A, AME2016B, mydata):
    # Compare experimental data with a linear model. Again, note that we use `_i`,
    # `_A`, and `_e` as variable names to keep them local to this cell. We could
    # (and probably should) write a function instead.
    aV = 8
    BindingLD = []
    for _i in range(0, len(mydata)):
        _A = AME2016A[_i]
        _e = aV * _A
        BindingLD.append(_e)
    plt.plot(AME2016A, BindingLD, '.', color='blue')
    plt.plot(AME2016A, AME2016B, '.', color='red')
    plt.axis([-20, 270, -200, 2000])
    plt.xlabel('Mass number A')
    plt.ylabel('Binding energy (MeV)')
    plt.text(50, 1000, 'Exp', color='red')
    plt.text(100, 500, 'Linear model', color='blue')
    plt.show()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## The origin of nuclear binding [arxiv.nucl-th/0301069](https://arxiv.org/abs/nucl-th/0301069), J.H. Rose et al. [PRL 53 (1984) 344](https://doi-org.libproxy.york.ac.uk/10.1103/PhysRevLett.53.344)
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.image(src="Lancaster.150825-09.slide41.png", alt="nuclear binding illustration")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Liquid-drop model and liquid-drop mass formula

    $$E_B(A,Z) = a_V A - a_S A^{\frac{2}{3}} - a_C \frac{Z^2}{A^{\frac{1}{3}}} - a_I \frac{(A-2Z)^2}{A} + \delta(A)$$

    $a_V$ is the volume energy coefficient

    $a_S$ is the surface energy coefficient

    $a_C$ is the Coulomb energy coefficient

    $a_I$ is the symmetry energy coefficient

    $\delta(A)$ is the pairing-energy term

    $$\delta(A) = \left\{\begin{array}{ll}
                           a_P A^{-3/4} & for~even-even~nuclei \\
                           0            & for~odd~nuclei \\
                           -a_P A^{-3/4} & for~odd-odd~nuclei \\
                           \end{array}\right.$$
    """)
    return


@app.cell
def _(AME2016A, AME2016B, AME2016N, AME2016Z, mydata):
    # Generating the liquid-drop parameters

    # values given in the 1980 book of Ring & Schuck,
    # "The Nuclear Many-Body Problem", Springer-Verlag, Berlin, 1980

    aV_1 = 15.98
    aS = 18.56
    aC = 0.717
    aI = 28.1
    aP = 34

    # Generating the liquid-drop binding energies

    BindingLD_1 = []
    for _i in range(0, len(mydata)):
        _A = AME2016A[_i]
        _N = AME2016N[_i]
        _Z = AME2016Z[_i]
        _e = aV_1 * _A - aS * _A ** twothird - aC * _Z ** 2 / _A ** onethird - aI * (_A - 2 * _Z) ** 2 / _A
        if _N % 2 == 0 and _Z % 2 == 0:
            _e = _e + aP * _A ** (-threefourth)
        if _N % 2 == 1 and _Z % 2 == 1:
            _e = _e - aP * _A ** (-threefourth)
        BindingLD_1.append(_e)
    plt.plot(AME2016A, BindingLD_1, '.', color='blue')
    plt.plot(AME2016A, AME2016B, '.', color='red')
    plt.axis([-20, 270, -200, 2000])
    plt.xlabel('Mass number A')
    plt.ylabel('Binding energy (MeV)')
    plt.text(50, 1000, 'Exp', color='red')
    plt.text(100, 500, 'Liquid Drop', color='blue')
    plt.show()
    return BindingLD_1, aC, aI, aP, aS, aV_1


@app.cell
def _(aC, aI, aP, aS, aV_1):
    BindingLDatA = []

    _N = 126
    _Z = 82
    _A = _N + _Z
    eV = aV_1 * _A
    eS = aS * _A ** twothird
    eC = aC * _Z ** 2 / _A ** onethird
    eI = aI * (_A - 2 * _Z) ** 2 / _A
    eP = 0
    if _N % 2 == 0 and _Z % 2 == 0:
        eP = +aP * _A ** (-threefourth)
    if _N % 2 == 1 and _Z % 2 == 1:
        eP = -aP * _A ** (-threefourth)

    BindingLDatA.append(eV)
    BindingLDatA.append(eS)
    BindingLDatA.append(eC)
    BindingLDatA.append(eI)

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = ['Volume', 'Surface', 'Coulomb', 'Symmetry']
    sizes = [eV, eS, eC, eI]
    explode = (0, 0, 0, 0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # The Symmetry Energy

    Let us have a look at the chain of isobars (nuclei having the same mass number A), which have the same volume and surface energies.
    """)
    return


@app.cell
def _(AME2016A, AME2016B, AME2016Z, BindingLD_1, mydata):
    # Generating data for the isobaric A=120 chain

    AME2016B120 = []
    AME2016Z120 = []
    LDB120 = []
    for _i in range(0, len(mydata)):
        _A = AME2016A[_i]
        if _A == 120:
            AME2016B120.append(AME2016B[_i])
            AME2016Z120.append(AME2016Z[_i])
            LDB120.append(BindingLD_1[_i])

    plt.plot(AME2016Z120, LDB120, '.', color='blue')
    plt.plot(AME2016Z120, AME2016B120, 'o', color='red')
    plt.axis([45, 57, 920, 1150])
    plt.xlabel('Atomic number Z')
    plt.ylabel('Binding energy (MeV)')
    plt.show()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # The Pairing Energy

    Odd-even mass staggering.

    $$OES_N(N,Z)=E_B(N,Z)-\frac{1}{2}\left(E_B(N+1,Z)+E_B(N-1,Z)\right)$$

    $$OES_Z(N,Z)=E_B(N,Z)-\frac{1}{2}\left(E_B(N,Z+1)+E_B(N,Z-1)\right)$$
    """)
    return


@app.cell
def _(AME2016B, AME2016N, AME2016Z, BindingLD_1, mydata):
    # Generating data for the odd-even staggering in the isotopic chain Z=68 (erbium)

    AME2016N68 = []
    AME2016n68 = []
    AME2016B68 = []
    LDB68 = []
    AME2016b68 = []
    LDb68 = []
    AME2016S68 = []
    LDS68 = []

    for _i in range(0, len(mydata)):
        _Z = AME2016Z[_i]
        if _Z == 68:
            AME2016B68.append(AME2016B[_i])
            AME2016n68.append(AME2016N[_i])
            LDB68.append(BindingLD_1[_i])

    for _i in range(1, len(LDB68) - 1):
        am = AME2016B68[_i - 1]
        a0 = AME2016B68[_i]
        ap = AME2016B68[_i + 1]
        AME2016S68.append(a0 - (am + ap) / 2)
        am = LDB68[_i - 1]
        a0 = LDB68[_i]
        ap = LDB68[_i + 1]
        LDS68.append(a0 - (am + ap) / 2)
        AME2016N68.append(AME2016n68[_i])

    plt.plot(AME2016N68, LDS68, '-', color='blue')
    plt.plot(AME2016N68, AME2016S68, '-', color='red')
    plt.axis([76, 105, -2, 2])
    plt.xlabel('Neutron number N')
    plt.ylabel('Odd-even mass staggering (MeV)')
    plt.show()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Residuals of the liquid-drop mass formula

    Differences between theory (model) and experiment
    """)
    return


@app.cell
def _(AME2016A, AME2016B, AME2016N, AME2016Z, mydata):
    # Generating the liquid-drop parameters

    # values given in the 1980 book of Ring & Schuck

    aV_2 = 15.98
    aS_1 = 18.56
    aC_1 = 0.717
    aI_1 = 28.1
    aP_1 = 34

    # Generating the liquid-drop binding energies

    _RMSdeviation = 0
    _ResidualLD = []
    for _i in range(0, len(mydata)):
        _A = AME2016A[_i]
        _N = AME2016N[_i]
        _Z = AME2016Z[_i]
        _e = aV_2 * _A - aS_1 * _A ** twothird - aC_1 * _Z ** 2 / _A ** onethird - aI_1 * (_A - 2 * _Z) ** 2 / _A
        if _N % 2 == 0 and _Z % 2 == 0:
            _e = _e + aP_1 * _A ** (-threefourth)
        if _N % 2 == 1 and _Z % 2 == 1:
            _e = _e - aP_1 * _A ** (-threefourth)
        _ResidualLD.append(_e - AME2016B[_i])
        _RMSdeviation = _RMSdeviation + _ResidualLD[_i] ** 2

    _RMSdeviation = math.sqrt(_RMSdeviation / len(mydata))

    print('RMS deviation=', _RMSdeviation) # explicit message

    plt.plot(AME2016Z, _ResidualLD, '.', color='green')
    plt.axis([-20, 270, -100, 50])
    plt.axis([-20, 160, -100, 50])
    plt.axis([-20, 120, -120, 50])
    plt.xlabel('Neutron number N')
    plt.xlabel('Mass number A')
    plt.xlabel('Atomic number Z')
    plt.ylabel('Residual (MeV)')
    plt.show()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # 2020 parameterization of the liquid-drop mass formula

    published in:

    Bethe–Weizsäcker semiempirical mass formula coefficients 2019 update based on AME2016

    Djelloul Benzaid, Salaheddine Bentridi, Abdelkader Kerraci, Naima Amrani

    Nuclear Science and Techniques, [31:9, 3 January 2020](https://doi.org/10.1007/s41365-019-0718-8)

      $$\delta(A) = \left\{\begin{array}{ll}
                          a_P A^{-1/2} & for~even-even~nuclei \\
                          0            & for~odd~nuclei \\
                          -a_P A^{-1/2} & for~odd-odd~nuclei \\
                          \end{array}\right.$$
    """)
    return


@app.cell
def _(AME2016A, AME2016B, AME2016N, AME2016Z, mydata):
    # Generating the liquid-drop parameters

    # values given in the recent paper, Benzaid et al. (2020)

    aV_3 = 14.64
    aS_2 = 14.08
    aC_2 = 0.64
    aI_2 = 21.07
    aP_2 = 11.54

    # Generating the liquid-drop binding energies

    _RMSdeviation = 0
    _ResidualLD = []
    for _i in range(0, len(mydata)):
        _A = AME2016A[_i]
        _N = AME2016N[_i]
        _Z = AME2016Z[_i]
        _e = aV_3 * _A - aS_2 * _A ** twothird - aC_2 * _Z ** 2 / _A ** onethird - aI_2 * (_A - 2 * _Z) ** 2 / _A
        if _N % 2 == 0 and _Z % 2 == 0:
            _e = _e + aP_2 * _A ** (-onehalf)
        if _N % 2 == 1 and _Z % 2 == 1:
            _e = _e - aP_2 * _A ** (-onehalf)
        _ResidualLD.append(_e - AME2016B[_i])
        _RMSdeviation = _RMSdeviation + _ResidualLD[_i] ** 2
    _RMSdeviation = math.sqrt(_RMSdeviation / len(mydata))
    print('RMS deviation=', _RMSdeviation)
    plt.plot(AME2016N, _ResidualLD, '.', color='green')
    plt.axis([-20, 270, -25, 15])
    plt.axis([-20, 160, -25, 15])
    plt.xlabel('Mass number A')
    plt.xlabel('Neutron number N')
    plt.ylabel('Residual (MeV)')
    plt.show()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Nuclear DFT - a primer

    The binding energy $E$ is defined as an integral of the energy density ${\cal H}(r)$, which depends on the kinetic density $\tau(r)$ and particle density $\rho(r)$:

    $$E\equiv\int\,dr\,{\cal H}(r),\quad\mbox{for}\quad {\cal H}(r)=\frac{\hbar^2}{2m}\tau(r)-\frac{1}{2}C\rho^2(r),\quad \rho(r)=\sum_{i=1}^A \phi_i(r)\phi^*_i(r),\quad \tau(r)=\sum_{i=1}^A (\nabla\phi_i(r))(\nabla\phi^*_i(r))$$

    Density Functional Theory (DFT) is based on a variational method, whereupon the single-particle (Kohn-Sham) orbitals $\phi_i(r)$ are obtained as:

    $$\delta_{\phi^*_i(r)}E[\tau(r),\rho(r)]=0\quad\Longrightarrow \left[-\frac{\hbar^2}{2m}\Delta - C\rho(r) \right]\phi_i(r)=\epsilon_i\phi_i(r)$$

    DFT looks like a mean-field approximation, it smells like a mean-field approximation, and it seems to be a mean-field approximation, but $\color{red}{\mbox{DFT is NOT a mean-field approximation.}}$ There exists an EXACT functional $E[\rho(r)]$ for which DFT gives the EXACT energy and the EXACT density.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Mass table based on the UNEDF0 Skyrme density functional:

    M. Kortelainen et al., [Phys. Rev. C 82, 024313 (2010)](https://journals.aps.org/prc/abstract/10.1103/PhysRevC.82.024313)

    ## Download the mass table

    [Skyrme UNEDF0 even-even nuclei](http://massexplorer.frib.msu.edu/content/DFTMassTables.html)
    """)
    return


@app.cell
def _():
    UNEDF0k = []
    UNEDF0N = []
    UNEDF0Z = []
    UNEDF0A = []
    UNEDF0B = []

    mydata2 = np.loadtxt('All_Even-Even_Nuclei.UNEDF0-cut.txt')
    for _i in range(0, len(mydata2)):
        UNEDF0k.append(_i)
        UNEDF0Z.append(mydata2[_i][0])  #Python starts counting on 0
        UNEDF0N.append(mydata2[_i][1])
        UNEDF0A.append(mydata2[_i][2])
        UNEDF0B.append(mydata2[_i][3])

    for _i in range(0, len(mydata2)):
        UNEDF0B[_i] = -UNEDF0B[_i]

    len(mydata2)
    return UNEDF0B, UNEDF0N, UNEDF0Z, mydata2


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Database of calculated UNEDEF0 even-even nuclei 2243 entries
    """)
    return


@app.cell
def _(
    AME2016B,
    AME2016N,
    AME2016Z,
    UNEDF0B,
    UNEDF0N,
    UNEDF0Z,
    mydata,
    mydata2,
):
    ResidualUN = []
    ResidualA = []
    ResidualN = []
    ResidualZ = []
    BindingUN = []
    BindingAM = []

    for _i in range(0, len(mydata)):
        _N = AME2016N[_i]
        _Z = AME2016Z[_i]
        for j in range(0, len(mydata2)):
            if _N == UNEDF0N[j] and _Z == UNEDF0Z[j]:
                ResidualUN.append(UNEDF0B[j] - AME2016B[_i])
                ResidualA.append(_N + _Z)
                ResidualN.append(_N)
                ResidualZ.append(_Z)
                BindingUN.append(UNEDF0B[j])
                BindingAM.append(AME2016B[_i])

    _RMSdeviation = 0
    for _i in range(0, len(ResidualUN)):
        _RMSdeviation = _RMSdeviation + ResidualUN[_i] ** 2
    _RMSdeviation = math.sqrt(_RMSdeviation / len(ResidualUN))

    print('RMS deviation=', _RMSdeviation)

    plt.plot(ResidualN, ResidualUN, '.', color='green')
    plt.axis([-20, 270, -25, 15])
    plt.axis([-20, 160, -25, 15])
    plt.xlabel('Mass number A')
    plt.xlabel('Neutron number N')
    plt.ylabel('Residual (MeV)')
    plt.show()
    plt.plot(ResidualN, ResidualUN, '.', color='green')
    plt.axis([-20, 270, -25, 15])
    #plt.xlabel('Atomic number Z')
    plt.axis([-20, 160, -5, 7])
    plt.xlabel('Mass number A')
    plt.xlabel('Neutron number N')
    plt.ylabel('Residual (MeV)')
    plt.show()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Modern nuclear DFT + corrections:

    [arXiv2011.07904](https://arxiv.org/abs/2011.07904)

    [The European Physical Journal A volume 57, Article number: 333 (2021) ](https://link.springer.com/article/10.1140/epja/s10050-021-00642-1)
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.image("arXiv2011.07904.png")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    RMS error on the 2408 known masses of 661 keV
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Modern nuclear Liquid Drop + corrections:

    [Atomic Data and Nuclear Data Tables 109–110 (2016) 1–204](http://dx.doi.org/10.1016/j.adt.2015.10.002)
    """)
    return


@app.cell
def _():
    mo.image("AtomicDataandNuclearDataTables109-1.png")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The error of the mass model is 559.5 keV for 2149 nuclei
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Take-home messages

    Nucleon-nucleon potential has a minimum around 0.9 fm and therefore nuclear matter in equilibrium has a binding energy per particle of about 8 MeV.

    Nuclear binding energy (positive) can be described as a sum of five terms:

    1.  large positive volume term,
    2.  large negative surface term,
    3.  large negative Coulomb term,
    4.  relatively small negative symmetry term, and
    5.  small pairing term with alternating sign

    Coulomb and symmetry terms are responsible for the stability valey turning for large A towards more neutron-rich nuclei

    Pairing term is responsible for the odd-even mass staggering along isotopic and isotonic chains

    Liquid-drop mass formula describes experimental masses with the RMS deviation of about 5 MeV

    Modern nuclear DFT describes experimental masses with the RMS deviation of about 1.7 MeV

    With correctons, the modern nuclear DFT and liquid-drop mass formula describe experimental masses with the RMS deviation of about 0.6 MeV
    """)
    return


if __name__ == "__main__":
    app.run()
