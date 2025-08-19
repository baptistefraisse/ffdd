# **FFDD: Fission Fragments Decay for Dummies**  

The discovery of nuclear fission, in 1939, marked a turning point in physics. But it was the realization that fission emits neutrons that truly unlocked the potential for self-sustaining chain reactions. This raises a fundamental question: Why does nuclear fission release neutrons? 

## **Scope and disclaimer**  

**FFDD** is a lightweight and educational toolbox designed to **simulate neutron emission in fission**. Its primary purpose is **pedagogical**: it aims to help physics students understand the basic mechanisms behind neutron emissions in nuclear fission, by enabling them to perform **simple but reasonably accurate predictions fission fragments decay**.

While the toolbox captures key features of fission fragment decay, **many advanced phenomena are intentionally omitted**. These simplifications were made to keep the physics accessible without significantly impacting the **first-order behavior**. For advanced users interested in high-accuracy modeling, the final section of the documentation points to some missing physical processes in FFDD and more comprehensive codes.

**Disclaimer**: This code is not meant to compete with or replace high-fidelity simulation tools. It is not intended for precision nuclear data work or safety-critical applications.

## Quick start

Full documentation (installation, quick start, and concepts) is available on the FFDD website: http://127.0.0.1:8000/ffdd/physics/.

Clone the repository and install in editable mode (requires Python ≥3.10):

```bash
git clone https://github.com/baptistefraisse/ffdd.git
cd ffdd
pip install -e .
pip show ffdd
```

Run the example:

```bash
cd examples
python3 example.py
```

Then, implement your own studies in a dedicated folder. 

Here are some ideas to get you started:

- Study the influence of the emitted neutrons energy ($e_n$)
- Play with different energy sharing models (Fong or von Edigy)
- Explore the effect of the anisothermal coefficient ($R_T$)
- Look at neutron multiplicity ($\bar\nu$) vs. fragment mass ($A$) 
- And feel free to investigate anything else that catches your interest!

## Contact

Questions or feedback: fraisse@cua.edu.