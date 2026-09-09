"use client";

import { useEffect, useRef, useState } from "react";
import type { EvidenceScenario } from "../content/evidence";
import {
  clampPlaybackStep,
  presentationAnnotations,
} from "../content/playback.mjs";
import { RecordedTrajectory } from "./RecordedTrajectory";

// Frequent presentation updates are confined to this instrument. Editorial
// copy, final-run evidence, provenance and disclosures do not rerender per step.
export function RecordedInstrument({
  scenario,
  enhanced,
  autoPlayOnArrival,
}: {
  scenario: EvidenceScenario;
  enhanced: boolean;
  autoPlayOnArrival: boolean;
}) {
  const [playback, setPlayback] = useState({
    step: scenario.steps,
    playing: false,
  });
  const [reference, setReference] = useState(false);
  const [reducedMotion, setReducedMotion] = useState(false);
  const instrument = useRef<HTMLDivElement>(null);
  const touched = useRef(false);
  const arrivalPlayed = useRef(false);
  const annotation = presentationAnnotations[scenario.scenario_id];
  const current = scenario.trajectory[playback.step];
  const atEnd = playback.step === scenario.steps;

  // The component is keyed by scenario ID, so preference changes and timers
  // always refer to this exact recorded run. This never evaluates the trace.
  useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: reduce)");
    const frame = requestAnimationFrame(() => {
      setReducedMotion(media.matches);
      if (media.matches) arrivalPlayed.current = true;
    });
    const change = () => {
      setReducedMotion(media.matches);
      if (media.matches) {
        arrivalPlayed.current = true;
        setPlayback({ step: scenario.steps, playing: false });
      }
    };
    const visibility = () => {
      if (document.hidden)
        setPlayback((previous) => ({ ...previous, playing: false }));
    };
    // First replay begins when the visitor can see the instrument. A phone
    // retains the useful final trace until scrolling brings the plot into view.
    // Leaving the viewport pauses playback; re-entry never restarts it.
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) {
          setPlayback((previous) =>
            previous.playing ? { ...previous, playing: false } : previous,
          );
        } else if (
          entry.intersectionRatio >= 0.75 &&
          autoPlayOnArrival &&
          !arrivalPlayed.current &&
          !touched.current &&
          !media.matches &&
          !document.hidden
        ) {
          arrivalPlayed.current = true;
          setPlayback({ step: 0, playing: true });
        }
      },
      { threshold: [0, 0.75], rootMargin: "-78px 0px 0px 0px" },
    );
    if (instrument.current) observer.observe(instrument.current);
    media.addEventListener("change", change);
    document.addEventListener("visibilitychange", visibility);
    return () => {
      cancelAnimationFrame(frame);
      observer.disconnect();
      media.removeEventListener("change", change);
      document.removeEventListener("visibilitychange", visibility);
    };
  }, [autoPlayOnArrival, scenario.steps]);

  useEffect(() => {
    if (!playback.playing) return;
    const timer = window.setInterval(
      () =>
        setPlayback((previous) => {
          if (!previous.playing) return previous;
          const next = clampPlaybackStep(previous.step + 1, scenario.steps);
          return { step: next, playing: next < scenario.steps };
        }),
      220,
    );
    return () => window.clearInterval(timer);
  }, [playback.playing, scenario.steps]);

  const go = (step: number) => {
    touched.current = true;
    setPlayback({
      step: clampPlaybackStep(step, scenario.steps),
      playing: false,
    });
  };
  const togglePlay = () => {
    touched.current = true;
    setPlayback((previous) => ({
      step: previous.step === scenario.steps ? 0 : previous.step,
      playing: !previous.playing,
    }));
  };

  return (
    <div
      className="stage-instrument"
      id="recorded-run"
      ref={instrument}
      onPointerDownCapture={() => {
        touched.current = true;
      }}
      onKeyDownCapture={() => {
        touched.current = true;
      }}
    >
      <div className="field-title">
        <span className="v-mono">
          RECORDED TRAJECTORY / {scenario.scenario_id}
        </span>
        <span className="recording-state">
          <i aria-hidden="true" />
          {playback.playing ? "PLAYING RECORDING" : "RECORDING"}
        </span>
      </div>
      <RecordedTrajectory
        scenario={scenario}
        step={playback.step}
        showReference={reference}
        id="stage-trace"
      />
      <div className="position-readout">
        <span className="v-mono">
          STEP <strong>{String(playback.step).padStart(2, "0")}</strong>
          <span className="readout-total"> / {scenario.steps}</span>
        </span>
        <span className="v-mono">
          ROW {String(current[0]).padStart(2, "0")}{" "}
          <span aria-hidden="true">·</span> COL{" "}
          {String(current[1]).padStart(2, "0")}
        </span>
        <span className="frame-caption">
          {atEnd
            ? "End of recorded run"
            : playback.step === 0
              ? "Initial position"
              : annotation && playback.step >= annotation.firstRevisitStep
                ? "Repeated recorded states"
                : "Recorded position"}
        </span>
      </div>
      <div className="playback" id="run-controls">
        <label className="sr-only" htmlFor="trace-step">
          Recorded controller step
        </label>
        <input
          id="trace-step"
          type="range"
          min="0"
          max={scenario.steps}
          value={playback.step}
          aria-valuetext={`Step ${playback.step} of ${scenario.steps}, row ${current[0]}, column ${current[1]}`}
          disabled={!enhanced}
          onChange={(e) => go(Number(e.target.value))}
          style={
            {
              "--cursor": `${(playback.step / scenario.steps) * 100}%`,
            } as React.CSSProperties
          }
        />
        <div className="playback-actions">
          <div className="transport">
            <button
              disabled={!enhanced}
              onClick={togglePlay}
              aria-label={
                playback.playing
                  ? "Pause recorded trajectory"
                  : atEnd
                    ? "Replay recorded trajectory"
                    : "Play recorded trajectory"
              }
            >
              <span aria-hidden="true">{playback.playing ? "Ⅱ" : "▷"}</span>
              <span>
                {playback.playing ? "Pause" : atEnd ? "Replay" : "Play"}
              </span>
            </button>
            <button
              disabled={!enhanced || playback.step === 0}
              onClick={() => go(playback.step - 1)}
              aria-label="Previous recorded step"
            >
              ←
            </button>
            <button
              disabled={!enhanced || atEnd}
              onClick={() => go(playback.step + 1)}
              aria-label="Next recorded step"
            >
              →
            </button>
          </div>
          <button
            className="reference-toggle"
            aria-pressed={reference}
            disabled={!enhanced}
            onClick={() => setReference((p) => !p)}
          >
            <span className="toggle-dash" aria-hidden="true" />
            A* reference
            <span aria-hidden="true">{reference ? "−" : "+"}</span>
          </button>
        </div>
        <div className="playback-foot">
          <span>
            Replay of frozen coordinates ·{" "}
            {reducedMotion ? "motion reduced" : "illustrative timing"}
          </span>
          {annotation && (
            <button
              disabled={!enhanced}
              onClick={() => go(annotation.firstRevisitStep)}
            >
              Inspect first recurrence <span aria-hidden="true">↗</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
