# LLM and ML Flow Documentation

This document outlines the architecture and data flow for the FeedZenAI project, specifically focusing on how the Large Language Model (LLM) and Machine Learning (ML) components interact within the multi-agent system.

## High-Level Architecture

The system consists of a Chrome Extension that acts as the eyes and hands of the application, and a FastAPI Backend that serves as the brain. The backend employs an Orchestrator pattern to manage a pipeline of specialized agents.

### Core Technologies
- **LLM**: Gemini 2.0 Flash (for fast classification and recommendation generation).
- **External Data**: YouTube Data API v3 (for fetching real video alternatives).
- **Orchestration**: Custom Python-based agent pipeline.

## Detailed Flow Diagram

![LLM and ML Flow Diagram](./LLM_ML_FLOW.png)

The following Mermaid diagram illustrates the step-by-step processing of a video feed item, from the moment it appears on the user's screen to the final intervention decision.

```mermaid
flowchart TD
    %% Nodes
    User((User))
    
    subgraph Chrome_Extension [Chrome Extension]
        CS[Content Script]
        UI[UI Overlay]
    end
    
    subgraph Backend [FastAPI Backend]
        API[API Endpoint /analyze]
        Orch{Orchestrator}
        
        subgraph Agents [Agent Pipeline]
            FIA[Feed Ingestion Agent]
            CCA[Content Classification Agent]
            ASA[Addiction Scoring Agent]
            ROA[Recommendation Optimizer Agent]
            BMA[Behaviour Monitor Agent]
            CECA[Extension Control Agent]
        end
    end
    
    subgraph External_Services [External Services]
        Gemini[Gemini 2.0 Flash]
        YT_API[YouTube Data API]
    end

    %% Flow
    User -- Opens YouTube --> CS
    CS -- Scans DOM & Extracts Metadata --> API
    API -- Forward Request --> Orch
    
    %% Agent Pipeline Flow
    Orch -- 1. Raw Data --> FIA
    FIA -- Normalized Metadata --> Orch
    
    Orch -- 2. Metadata --> CCA
    CCA -- "Analyze Title/Context" --> Gemini
    Gemini -- "Category: Addictive/Educational" --> CCA
    CCA -- Classification Result --> Orch
    
    Orch -- 3. Class + Metadata --> ASA
    ASA -- Calculate Risk Score --> Orch
    
    Orch -- 4. Class + Score --> ROA
    ROA -- Check if Score > Threshold --> ROA_Check{High Risk?}
    
    ROA_Check -- Yes --> ROA_Gen
    ROA_Check -- No --> ROA_Skip[Skip Recommendations]
    
    ROA_Gen["Generate Search Query"] -- Prompt --> Gemini
    Gemini -- "Query: Python Tutorial" --> ROA_Gen
    ROA_Gen -- Search Videos --> YT_API
    YT_API -- Video List --> ROA
    ROA -- Alternatives --> Orch
    ROA_Skip -- Empty List --> Orch
    
    Orch -- 5. History + Score --> BMA
    BMA -- Check Daily Limits --> Orch
    
    Orch -- 6. All Context --> CECA
    CECA -- Generate UI Actions --> Orch
    
    %% Return Path
    Orch -- Final Response JSON --> API
    API -- HTTP 200 OK --> CS
    CS -- Apply Blur/Buttons --> UI
    UI -- "Watch Alternative" --> User
```

## Agent Roles & Data Transformation

| Agent | Input | Operation | Output |
|-------|-------|-----------|--------|
| **FIA** | Raw DOM elements | Normalization, Validation | Structured Metadata (Title, Duration, Channel) |
| **CCA** | Metadata | **LLM Call**: Classify intent (Clickbait vs. Educational) | Category, Confidence Score |
| **ASA** | Metadata, Category | Weighted Scoring Algorithm | Addiction Score (0-10), Risk Level |
| **ROA** | Category, Score | **LLM Call**: Generate productive query<br>**API Call**: Fetch YouTube videos | List of Alternative Videos |
| **BMA** | User History | Statistical Analysis | Daily Usage Stats, Warning Flags |
| **CECA**| All Agent Outputs | UI Logic Generation | JSON Instructions for Chrome Extension (Blur, Buttons) |

## Key Interactions

1.  **Classification (CCA)**: We use Gemini 2.0 Flash because it provides nuanced understanding of video titles that simple keyword matching cannot catch (e.g., distinguishing "Python Fails" from "Python Tutorial").
2.  **Recommendation (ROA)**: Instead of hallucinating video links, we use the LLM to *generate a search query* based on the user's interests (context), and then use the **YouTube Data API** to fetch *actual, playable videos*. This ensures 100% link validity.
3.  **Orchestration**: The Orchestrator manages the state between agents, ensuring that downstream agents (like ROA) have access to the outputs of upstream agents (like CCA and ASA).
