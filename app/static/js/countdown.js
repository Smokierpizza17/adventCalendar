function formatRemaining(ms) {
  const s = Math.floor(ms / 1000);
  const days = Math.floor(s / 86400);
  const hours = Math.floor((s % 86400) / 3600);
  const minutes = Math.floor((s % 3600) / 60);
  const seconds = s % 60;
  const pad = (n) => String(n).padStart(2, "0");

  const text = days > 0
    ? `${days}d ${pad(hours)}h ${pad(minutes)}m ${pad(seconds)}s`
    : `${pad(hours)}h ${pad(minutes)}m ${pad(seconds)}s`;

  return { text, hasDays: days > 0 };
}

function tickCountdowns() {
  const elements = document.querySelectorAll(".countdown[data-unlock]");
  let anyPending = false;

  elements.forEach((el) => {
    const unlockAt = new Date(el.dataset.unlock).getTime();
    const remaining = unlockAt - Date.now();

    if (remaining <= 0) {
      el.textContent = "unlocking…";
      el.classList.remove("has-days");
      if (!el.dataset.reloadQueued) {
        el.dataset.reloadQueued = "1";
        setTimeout(() => window.location.reload(), 1000);
      }
    } else {
      const { text, hasDays } = formatRemaining(remaining);
      el.textContent = text;
      el.classList.toggle("has-days", hasDays);
      anyPending = true;
    }
  });

  return anyPending;
}

function formatLocalUnlock(iso, { withZone }) {
  const date = new Date(iso);
  const pad = (n) => String(n).padStart(2, "0");

  const year = date.getFullYear();
  const month = pad(date.getMonth() + 1);
  const day = pad(date.getDate());
  const hour = pad(date.getHours());
  const minute = pad(date.getMinutes());

  let text = `${year}-${month}-${day} ${hour}:${minute}`;

  if (withZone) {
    const zone = new Intl.DateTimeFormat(undefined, { timeZoneName: "short" })
      .formatToParts(date)
      .find((part) => part.type === "timeZoneName").value;
    text += ` ${zone}`;
  }

  return text;
}

function renderLocalUnlockTimes() {
  document.querySelectorAll(".unlock-local[data-unlock]").forEach((el) => {
    // The day page (a <strong>) spells out the zone; grid tiles (a <span>) stay compact.
    const withZone = el.tagName === "STRONG";
    el.textContent = formatLocalUnlock(el.dataset.unlock, { withZone });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  renderLocalUnlockTimes();

  if (tickCountdowns()) {
    setInterval(tickCountdowns, 1000);
  }
});
