# Grouped Mermaid Graph Sample

This grouped graph is designed for the fuller Jomon / Dotaku / Kiki case.
It keeps genetics, archaeology, mythology, continental background, comparative methods,
narrative audit, and falsification visible as separate subgraphs.

```mermaid
graph TD
  subgraph Genetics
    P1[Sato / Inoue & Sato] --> SC1[Source claim: Y-lineage variation]
    SC1 --> E1[D1a2a/D-M55 high frequency]
    P2[Cooke / Liu] --> SC2[Source claim: updated ancestry models]
    SC2 --> E2[Autosomal ancestry models]
    E1 --> E3[Paternal/autosomal asymmetry]
    E2 --> E3
    E3 --> I1[Paternal asymmetry inference]
    A1[Assumption: Y-lines may preserve social signal] --> I1
    I1 --> UC1[Possible paternal social advantage]
  end

  subgraph Archaeology
    P3[Hudson 1992] --> E4[Dotaku discontinuity]
    P4[Mabuchi & Hirao] --> E5[External bronze-source networks]
    E4 --> I2[Social reorganization inference]
    E5 --> I2
    A2[Assumption: ritual discontinuity may signal reorganization] --> I2
    I2 --> UC2[Possible network disruption / ritual transfer]
  end

  subgraph Mythology
    P5[Kojiki / Nihon Shoki] --> E6[Descent, land transfer, Ogetsuhime motifs]
    E6 --> I3[Myth-as-social-memory inference]
    A3[Assumption: myth can preserve transformed memory] --> I3
    I3 --> UC3[Possible ritual-political memory]
  end

  subgraph Continental_Background
    P6[Fang / Liu / Wang] --> E7[Shandong-Haidai / coastal gene flow]
    P7[Fujio chronology] --> E8[Yayoi chronology]
    E7 --> I4[Continental context inference]
    E8 --> I4
    I4 --> UC4[Context, not direct cause]
  end

  subgraph Cross_Domain_Model
    UC1 --> UC5[Integrated abductive model]
    UC2 --> UC5
    UC3 --> UC5
    UC4 --> UC5
    M1[Abductive reasoning] -. not evidence .-> UC5
    M3[Consilience] -. not evidence .-> UC5
    M8[Falsification framing] -. not evidence .-> UC5
  end

  subgraph Narrative_Audit
    N1[Standard overlay narrative]
    N2[Passive survival narrative]
    N3[Internal dotaku transition narrative]
    N4[Myth as literary legitimation narrative]
    N5[Simplified migration narrative]
    UC1 -- challenges narrative --> N1
    UC1 -- challenges narrative --> N2
    UC2 -- challenges narrative --> N3
    UC3 -- challenges narrative --> N4
    UC4 -- challenges narrative --> N5
  end

  subgraph Comparative_Methods
    M4[Myth as social memory, not chronicle] -. heuristic .-> UC3
    M6[Kumulipo / oral genealogy analogy] -. heuristic .-> UC3
    M7[Comparative highland/lowland history] -. heuristic .-> UC2
    M7 -. heuristic .-> UC3
  end

  subgraph Falsification_and_Risks
    R1[Y-DNA alone cannot prove dominance] -. qualifies .-> UC1
    R2[Dotaku discontinuity cannot prove takeover] -. qualifies .-> UC2
    R3[Myth is not chronicle] -. qualifies .-> UC3
    R4[No direct Shang-Zhou-to-Yayoi causal proof] -. qualifies .-> UC4
    R5[Do not call Dotaku sphere simply immigrant] -. qualifies .-> UC5
    F1[Kofun elite aDNA test] -. weakens .-> UC1
    F2[Dotaku continuity test] -. weakens .-> UC2
    F3[Kiki late-construction test] -. weakens .-> UC3
    F4[Ancient DNA source-model test] -. weakens .-> UC4
  end
```
