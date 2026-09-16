function formatRemaining(ms) {
  const s = Math.floor(ms / 1000);
  const days = Math.floor(s / 86400);
  const hours = Math.floor((s % 86400) / 3600);
  const minutes = Math.floor((s % 3600) / 60);
  const seconds = s % 60;
  const pad = (n) => String(n).padStart(2, "0");

  const text = days > 0
    ? `${days}d ${pad(hours)}h ${pad(minutes)}m`
    : hours > 0
    ? `${pad(hours)}h ${pad(minutes)}m ${pad(seconds)}s`
    : `${pad(minutes)}m ${pad(seconds)}s`;

  return { text, hasDays: days > 0 };
}

const URGENT_THRESHOLD_MS = 60 * 60 * 1000;

function tickCountdowns() {
  const elements = document.querySelectorAll(".countdown[data-unlock]");
  let anyPending = false;

  elements.forEach((el) => {
    const unlockAt = new Date(el.dataset.unlock).getTime();
    const remaining = unlockAt - Date.now();

    if (remaining <= 0) {
      el.textContent = "unlocking…";
      el.classList.remove("has-days", "urgent");
      if (!el.dataset.reloadQueued) {
        el.dataset.reloadQueued = "1";
        setTimeout(() => window.location.reload(), 1000);
      }
    } else {
      const { text, hasDays } = formatRemaining(remaining);
      el.textContent = text;
      el.classList.toggle("has-days", hasDays);
      el.classList.toggle("urgent", remaining < URGENT_THRESHOLD_MS);
      anyPending = true;
    }
  });

  return anyPending;
}

function formatLocalUnlock(iso) {
  const date = new Date(iso);
  const pad = (n) => String(n).padStart(2, "0");

  const hour = pad(date.getHours());
  const minute = pad(date.getMinutes());
  const time = `${hour}:${minute}`;

  const startOfDay = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate());
  const dayDiff = Math.round((startOfDay(date) - startOfDay(new Date())) / 86400000);

  if (dayDiff === 0) {
    return time;
  }
  if (dayDiff > 0 && dayDiff <= 6) {
    const weekday = new Intl.DateTimeFormat(undefined, { weekday: "short" }).format(date);
    return `${weekday} ${time}`;
  }
  const day = pad(date.getDate());
  const month = pad(date.getMonth() + 1);
  return `${day}.${month}. ${time}`;
}

function renderLocalUnlockTimes() {
  document.querySelectorAll(".unlock-local[data-unlock]").forEach((el) => {
    el.textContent = formatLocalUnlock(el.dataset.unlock);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  renderLocalUnlockTimes();

  if (tickCountdowns()) {
    setInterval(tickCountdowns, 1000);
  }
});
