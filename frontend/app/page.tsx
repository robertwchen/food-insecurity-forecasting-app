"use client";

import { FormEvent, useState } from "react";

const BACKEND_URL = "http://127.0.0.1:8000";

type FormValues = {
  month: string;
  population: string;
  snapParticipants: string;
  unemployedPeople: string;
  peopleBelowPoverty: string;
  previousMonthFoodLbs: string;
};

type PredictionResponse = {
  predicted_food_lbs: number;
  features_used: Record<string, number>;
};

const INITIAL_FORM: FormValues = {
  month: "6",
  population: "100000",
  snapParticipants: "12000",
  unemployedPeople: "4500",
  peopleBelowPoverty: "15000",
  previousMonthFoodLbs: "70000",
};

export default function HomePage() {
  const [form, setForm] = useState<FormValues>(INITIAL_FORM);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  function updateField(field: keyof FormValues, value: string) {
    setForm((current) => ({
      ...current,
      [field]: value,
    }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setResult(null);
    setIsSubmitting(true);

    try {
      const response = await fetch(`${BACKEND_URL}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          month: Number(form.month),
          population: Number(form.population),
          snap_participants: Number(form.snapParticipants),
          unemployed_people: Number(form.unemployedPeople),
          people_below_poverty: Number(form.peopleBelowPoverty),
          previous_month_food_lbs: Number(form.previousMonthFoodLbs),
        }),
      });

      if (!response.ok) {
        throw new Error("Prediction request failed.");
      }

      const data = (await response.json()) as PredictionResponse;
      setResult(data);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Something went wrong while calling the backend.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="hero">
        <p className="eyebrow">Food Insecurity Forecasting</p>
        <h1>Predict monthly food distribution needs</h1>
        <p className="hero-copy">
          This frontend collects user inputs, sends them to the FastAPI backend,
          and shows the prediction returned by the trained model.
        </p>
      </section>

      <section className="card">
        <h2>Prediction form</h2>
        <form className="form-grid" onSubmit={handleSubmit}>
          <label>
            Month
            <input
              min="1"
              max="12"
              type="number"
              value={form.month}
              onChange={(event) => updateField("month", event.target.value)}
              required
            />
          </label>

          <label>
            Population
            <input
              min="1"
              type="number"
              value={form.population}
              onChange={(event) => updateField("population", event.target.value)}
              required
            />
          </label>

          <label>
            SNAP participants
            <input
              min="0"
              type="number"
              value={form.snapParticipants}
              onChange={(event) =>
                updateField("snapParticipants", event.target.value)
              }
              required
            />
          </label>

          <label>
            Unemployed people
            <input
              min="0"
              type="number"
              value={form.unemployedPeople}
              onChange={(event) =>
                updateField("unemployedPeople", event.target.value)
              }
              required
            />
          </label>

          <label>
            People below poverty
            <input
              min="0"
              type="number"
              value={form.peopleBelowPoverty}
              onChange={(event) =>
                updateField("peopleBelowPoverty", event.target.value)
              }
              required
            />
          </label>

          <label>
            Previous month food (lbs)
            <input
              min="0"
              type="number"
              value={form.previousMonthFoodLbs}
              onChange={(event) =>
                updateField("previousMonthFoodLbs", event.target.value)
              }
              required
            />
          </label>

          <button className="submit-button" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Predicting..." : "Get prediction"}
          </button>
        </form>

        {error ? <p className="error-text">{error}</p> : null}

        {result ? (
          <div className="result-panel">
            <h3>Prediction result</h3>
            <p className="prediction-value">
              {result.predicted_food_lbs.toLocaleString(undefined, {
                maximumFractionDigits: 2,
              })}{" "}
              lbs
            </p>

            <h4>Features used by the backend</h4>
            <ul className="feature-list">
              {Object.entries(result.features_used).map(([key, value]) => (
                <li key={key}>
                  <span>{key}</span>
                  <strong>{value}</strong>
                </li>
              ))}
            </ul>
          </div>
        ) : null}
      </section>
    </main>
  );
}
