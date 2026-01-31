# References — NARS & Counterfactual Reasoning Research

---

## Primary Sources

### Deep Structural Causal Models
- **Pawlowski, N., Ktena, S.I., Thomson, M., Vlontzos, A., Rueckert, D., Glocker, B.** (2020). "Deep Structural Causal Models for Tractable Counterfactual Inference." *NeurIPS 2020*.
  - Paper: https://proceedings.neurips.cc/paper/2020/file/0987b8b338d6c90bbedd8631bc499221-Paper.pdf
  - Framework: Pearl's SCM + normalizing flows for tractable counterfactual inference
  - Key contribution: Solves abduction problem via invertible transformations

### NARS — Non-Axiomatic Reasoning System
- **Wang, Pei** (2012). "AGI-NARS Course Materials." *Temple University CIS Department*.
  - Course: https://cis.temple.edu/~pwang/AGI-NARS/2012-PKU/index.html
  - Slides: https://cis.temple.edu/~pwang/AGI-NARS/2012-PKU/slides/
  - Book: "Non-Axiomatic Logic: A Model of Intelligent Reasoning" (World Scientific, 2013)
  - Key contribution: AIKR, NAL-7 temporal copulas, causation as acquired concept

### XAI Counterfactual Explanations
- **Molnar, C. & Dandl, S.** "Counterfactual Explanations." *Interpretable Machine Learning*, Chapter 15.
  - URL: https://christophm.github.io/interpretable-ml-book/counterfactual.html
  - Key contribution: Comprehensive treatment of methods, four criteria, practical applications

- **Wachter, S., Mittelstadt, B., Russell, C.** (2018). "Counterfactual Explanations Without Opening the Black Box: Automated Decisions and the GDPR." *Harvard Journal of Law & Technology*, 31(2).
  - Key contribution: Loss function formulation, MAD-weighted distance

- **Dandl, S., Molnar, C., Binder, M., Bischl, B.** (2020). "Multi-Objective Counterfactual Explanations." *PPSN XVI*.
  - GitHub: https://github.com/susanne-207/moc
  - Key contribution: Four objectives, NSGA-II optimization, Pareto-optimal sets

## Additional Sources

### Counterfactual XAI Medium Article
- **Inkollu Sri Varsha** (2025). "Untangling the 'What Ifs': A Guide to Counterfactual Explanations in AI." *Medium*.
  - URL: https://medium.com/@inkollusrivarsha0287/untangling-the-what-ifs-a-guide-to-counterfactual-explanations-in-ai-2273a2824b5
  - Covers: DiCE framework, practical examples, GDPR compliance

### Software Implementations
- **DiCE** (Microsoft): https://github.com/interpretml/DiCE — Diverse Counterfactual Explanations via determinantal point processes
- **Alibi** (SeldonIO): https://github.com/SeldonIO/alibi — Simple + prototype-based counterfactual methods
- **MACE** (Karimi et al.): https://github.com/amirhk/mace — Satisfiability solver approach
- **MOC** (Dandl et al.): https://github.com/susanne-207/moc — Multi-objective counterfactual implementation (R)

### Foundational Works (Referenced)
- **Pearl, J.** (2009). *Causality: Models, Reasoning, and Inference*. 2nd ed. Cambridge University Press.
- **Pearl, J.** (2000). "The Ladder of Causation" — Association → Intervention → Counterfactual
- **Laugel, T. et al.** (2017). "Inverse Classification for Comparison-Based Interpretability in Machine Learning." — Growing Spheres method
- **Karimi, A.H. et al.** (2020). "Algorithmic Recourse: From Counterfactual Explanations to Interventions." — MACE framework
- **Deb, K. et al.** (2002). "A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II." — NSGA-II algorithm used by Dandl

## Ada Architecture Files Analyzed

From `ada-consciousness/core/`:
- `agi_lego_party_canonical.yaml` — 1263 lines — Epistemic atoms, operators, 36 styles, macros, recombination engine
- `consciousness_runtime.py` — 667 lines — Tick loop, ghost tracking, soul integration, dream modes
- `gql_search.py` — 1172 lines — DN parsing, ISA resolution, Levenshtein association, GQL search, Cypher
- `thinking_styles_36.py` — 815 lines — 36 styles, 9 RI channels, ResonanceEngine

## Research Session Transcripts

All work preserved in:
- `/mnt/transcripts/2026-01-31-05-52-32-ada-nars-comparison-analysis.txt` — Ada vs OpenNARS deep comparison
- `/mnt/transcripts/2026-01-31-06-01-22-deep-scm-nars-counterfactual-research.txt` — Three-source counterfactual research
- `/mnt/transcripts/2026-01-31-06-13-16-counterfactual-research-synthesis.txt` — Comprehensive synthesis + docx generation
- `/mnt/transcripts/2026-01-31-09-17-35-counterfactual-xai-molnar-integration.txt` — Molnar chapter integration + Ada architecture analysis
