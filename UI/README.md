# Week 6 + Week 7 Combined: Impact Predictor UI Prototype

This prototype combines:
- Week 6: simple UI form for impact/risk prediction
- Week 7: edge-case testing and logic improvements

It uses the best-performing saved model from your previous evaluation run:
- `saved_models/gb_custom.pkl`

## Features
- Retro black-and-white UI theme
- Landing page and basic login flow (no authentication)
- Input validation + clamping for robust behavior
- Automatic `depth_mag_ratio` computation for consistent feature engineering
- Prediction outputs:
  - Predicted alert class (`green/yellow/orange/red`)
  - Impact score (0-100)
  - Risk level (`Low/Moderate/High/Severe`)
  - Class probability breakdown
- Predicted target class shown with its color badge
- Result panel shake intensity increases with risk level
- Built-in edge-case tests

## Run
From workspace root:

```powershell
python week6_7_impact_predictor/app.py
```

Open:
- http://127.0.0.1:5000 (landing page)

Flow:
- Landing page: `/`
- Login page: `/login`
- Predictor app: `/app`

## Run Week 7 Edge-Case Tests

```powershell
python week6_7_impact_predictor/app.py --run-tests
```

Or use endpoint:
- http://127.0.0.1:5000/tests
