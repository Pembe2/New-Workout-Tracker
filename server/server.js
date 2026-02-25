const path = require("path");
const crypto = require("crypto");
const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const bcrypt = require("bcryptjs");

const app = express();
const PORT = process.env.PORT || 3000;
const DB_PATH = process.env.DB_PATH || path.join(__dirname, "workout.db");
const TOKEN_TTL_DAYS = 30;

app.use(express.json({ limit: "2mb" }));

// CORS for file:// origin or alternate hosts
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  if (req.method === "OPTIONS") return res.sendStatus(204);
  next();
});

const db = new sqlite3.Database(DB_PATH);

function run(sql, params = []) {
  return new Promise((resolve, reject) => {
    db.run(sql, params, function (err) {
      if (err) return reject(err);
      resolve(this);
    });
  });
}

function get(sql, params = []) {
  return new Promise((resolve, reject) => {
    db.get(sql, params, (err, row) => {
      if (err) return reject(err);
      resolve(row || null);
    });
  });
}

function all(sql, params = []) {
  return new Promise((resolve, reject) => {
    db.all(sql, params, (err, rows) => {
      if (err) return reject(err);
      resolve(rows || []);
    });
  });
}

async function initDb() {
  await run(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT NOT NULL UNIQUE,
      password_hash TEXT NOT NULL,
      created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );
  `);
  await run(`
    CREATE TABLE IF NOT EXISTS sessions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      token TEXT NOT NULL UNIQUE,
      expires_at TEXT NOT NULL,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      FOREIGN KEY(user_id) REFERENCES users(id)
    );
  `);
  await run(`
    CREATE TABLE IF NOT EXISTS workouts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      workout_key TEXT NOT NULL,
      data_json TEXT NOT NULL,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      UNIQUE(user_id, workout_key),
      FOREIGN KEY(user_id) REFERENCES users(id)
    );
  `);
}

function createToken() {
  return crypto.randomBytes(32).toString("hex");
}

function expiryDate(days) {
  const d = new Date();
  d.setDate(d.getDate() + days);
  return d.toISOString();
}

async function createSession(userId) {
  const token = createToken();
  const expiresAt = expiryDate(TOKEN_TTL_DAYS);
  await run(
    "INSERT INTO sessions (user_id, token, expires_at) VALUES (?, ?, ?)",
    [userId, token, expiresAt]
  );
  return { token, expiresAt };
}

async function authMiddleware(req, res, next) {
  try {
    const header = req.headers.authorization || "";
    const token = header.startsWith("Bearer ") ? header.slice(7) : null;
    if (!token) return res.status(401).json({ error: "Missing token" });
    const session = await get(
      "SELECT id, user_id, token, expires_at FROM sessions WHERE token = ?",
      [token]
    );
    if (!session) return res.status(401).json({ error: "Invalid token" });
    if (new Date(session.expires_at) < new Date()) {
      await run("DELETE FROM sessions WHERE id = ?", [session.id]);
      return res.status(401).json({ error: "Session expired" });
    }
    const user = await get("SELECT id, username FROM users WHERE id = ?", [
      session.user_id,
    ]);
    if (!user) return res.status(401).json({ error: "User not found" });
    req.user = user;
    req.session = session;
    next();
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
}

app.get("/api/health", (req, res) => {
  res.json({ ok: true, time: new Date().toISOString() });
});

app.post("/api/register", async (req, res) => {
  try {
    const { username, password } = req.body || {};
    if (!username || !password) {
      return res.status(400).json({ error: "Username and password required" });
    }
    if (String(username).length < 3 || String(password).length < 6) {
      return res
        .status(400)
        .json({ error: "Username 3+ chars, password 6+ chars" });
    }
    const existing = await get("SELECT id FROM users WHERE username = ?", [
      username,
    ]);
    if (existing) return res.status(409).json({ error: "User exists" });
    const hash = await bcrypt.hash(String(password), 10);
    const result = await run(
      "INSERT INTO users (username, password_hash) VALUES (?, ?)",
      [username, hash]
    );
    const session = await createSession(result.lastID);
    res.json({ token: session.token, username });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

app.post("/api/login", async (req, res) => {
  try {
    const { username, password } = req.body || {};
    if (!username || !password) {
      return res.status(400).json({ error: "Username and password required" });
    }
    const user = await get(
      "SELECT id, username, password_hash FROM users WHERE username = ?",
      [username]
    );
    if (!user) return res.status(401).json({ error: "Invalid credentials" });
    const ok = await bcrypt.compare(String(password), user.password_hash);
    if (!ok) return res.status(401).json({ error: "Invalid credentials" });
    const session = await createSession(user.id);
    res.json({ token: session.token, username: user.username });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

app.post("/api/logout", authMiddleware, async (req, res) => {
  try {
    await run("DELETE FROM sessions WHERE id = ?", [req.session.id]);
    res.json({ ok: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

app.get("/api/me", authMiddleware, async (req, res) => {
  res.json({ id: req.user.id, username: req.user.username });
});

app.get("/api/workouts/:key", authMiddleware, async (req, res) => {
  try {
    const workoutKey = String(req.params.key || "");
    if (!workoutKey) return res.status(400).json({ error: "Missing key" });
    const row = await get(
      "SELECT data_json, updated_at FROM workouts WHERE user_id = ? AND workout_key = ?",
      [req.user.id, workoutKey]
    );
    if (!row) return res.status(404).json({ error: "Not found" });
    res.json({ data: JSON.parse(row.data_json), updated_at: row.updated_at });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

app.post("/api/workouts/:key", authMiddleware, async (req, res) => {
  try {
    const workoutKey = String(req.params.key || "");
    const data = req.body && req.body.data;
    if (!workoutKey) return res.status(400).json({ error: "Missing key" });
    if (!data || typeof data !== "object") {
      return res.status(400).json({ error: "Missing data" });
    }
    const now = new Date().toISOString();
    await run(
      `
      INSERT INTO workouts (user_id, workout_key, data_json, created_at, updated_at)
      VALUES (?, ?, ?, ?, ?)
      ON CONFLICT(user_id, workout_key)
      DO UPDATE SET data_json = excluded.data_json, updated_at = excluded.updated_at
      `,
      [req.user.id, workoutKey, JSON.stringify(data), now, now]
    );
    res.json({ ok: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

app.use(express.static(path.join(__dirname, "..")));

initDb()
  .then(() => {
    app.listen(PORT, () => {
      console.log(`Server running on http://localhost:${PORT}`);
    });
  })
  .catch((err) => {
    console.error("Failed to init db", err);
    process.exit(1);
  });
