# HR Analytics & Employee Mobility

is a Streamlit dashboard for exploring candidate and employee profiles, analyzing patterns associated with job-change intent, and estimating flight risk with a trained XGBoost pipeline. It combines interactive data exploration and visual analysis with an individual profile prediction page.

## Project features

- **Dataset overview:** Review dataset metrics, field definitions, distributions, and sample records.
- **Workforce analysis:** Explore mobility and attrition patterns across career stages, education, experience, and other profile attributes.
- **Flight-risk prediction:** Enter a profile to get a model-based estimate of job-change intent.

## Dataset

The app reads [`Cleaned_df.csv`](./Cleaned_df.csv), a dataset of **19,044 records and 14 columns**. Each row represents a candidate or employee profile. The target distribution is:

| `Target` | Meaning | Records | Share |
| --- | --- | ---: | ---: |
| `0` | Not seeking a job change | 14,302 | 75.1% |
| `1` | Seeking a job change | 4,742 | 24.9% |

The dataset includes:

- **Location:** `City`, `City_development_index`
- **Profile and education:** `Gender`, `Education_level`, `Major_discipline`, `Enrolled_university`
- **Work history:** `Relevent_experience`, `Experience`, `Last_new_job`, `Career_Stage`
- **Employer and training:** `Company_size`, `Company_type`, `Training_hours`
- **Prediction label:** `Target`

Some profile and employer fields contain missing values, including `Company_size`, `Company_type`, `Gender`, and `Major_discipline`. The dashboard should be interpreted as exploratory analysis and model-assisted decision support, not as a definitive assessment of any individual.

## Run locally

Use Python with the packages listed in [`requirements.txt`](./requirements.txt):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run Home.py
```

The predictor page also relies on the saved model and input assets `XGBoost Pipeline.joblib` and `Inputs.pkl`, which should remain in the project root.
