async function fetchHabits() {
  try {
    const response = await fetch("/api/habits");
    if (!response.ok) throw new Error('Failed to fetch');
    const habits = await response.json();
    renderHabits(habits);
  } catch (e) {
    console.error(e);
    alert('Error loading habits. Check console for details.');
  }
}

function renderHabits(habits) {
  const list = document.getElementById("habitsList");
  list.innerHTML = "";

  habits.forEach((habit) => {
    const card = document.createElement("div");
    card.className = "habit-card";

    const isCompleted = habit.completed_today ? "completed" : "";
    const checkIcon = habit.completed_today ? "✓" : "";

    // Prepare chart data (last 7 days)
    const labels = [];
    const dataPoints = [];
    const today = new Date();

    for (let i = 6; i >= 0; i--) {
      const d = new Date();
      d.setDate(today.getDate() - i);
      const dateStr = d.toISOString().split("T")[0];
      labels.push(d.toLocaleDateString("en-US", { weekday: "narrow" }));
      dataPoints.push(habit.logs.includes(dateStr) ? 1 : 0);
    }

    const canvasId = `chart-${habit.id}`;

    card.innerHTML = `
            <div class="habit-header">
                <div>
                    <div class="habit-name">${habit.name}</div>
                    <div class="streak-badge">🔥 ${habit.streak} day streak</div>
                </div>
                <div class="habit-actions">
                    <button class="check-btn ${isCompleted}" onclick="toggleLog(${habit.id})">
                        ${checkIcon}
                    </button>
                    <button class="delete-btn" onclick="deleteHabit(${habit.id})">✕</button>
                </div>
            </div>
            <div class="chart-container">
                <canvas id="${canvasId}"></canvas>
            </div>
        `;
    list.appendChild(card);

    // Render Chart
    const ctx = document.getElementById(canvasId).getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            data: dataPoints,
            backgroundColor: habit.completed_today
              ? "#4caf50"
              : "rgba(255, 255, 255, 0.2)",
            borderRadius: 4,
            barThickness: 10,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: "#b0b0b0" },
          },
          y: { display: false, max: 1 },
        },
      },
    });
  });
}

async function addHabit() {
  const input = document.getElementById("habitName");
  const name = input.value.trim();
  if (!name) return;

  await fetch("/api/habits", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });

  input.value = "";
  fetchHabits();
}

async function toggleLog(habitId) {
  await fetch("/api/logs", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ habit_id: habitId }),
  });
  fetchHabits();
}

async function deleteHabit(habitId) {
  if (!confirm("Are you sure?")) return;
  await fetch(`/api/habits/${habitId}`, { method: "DELETE" });
  fetchHabits();
}

// Initial load
fetchHabits();
