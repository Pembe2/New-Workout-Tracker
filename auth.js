(() => {
  const SUPABASE_URL = "https://gsczpbjpsyjygxirgzsy.supabase.co";
  const SUPABASE_ANON_KEY = "sb_publishable_o_naUNG0pM4nhzeU6k35eg_qbNGoIkg";

  if (!window.supabase) {
    throw new Error("Supabase client not loaded. Add the CDN script first.");
  }

  const { createClient } = window.supabase;
  const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
  let cachedSession = null;
  let cachedUser = null;

  async function init() {
    const { data, error } = await supabase.auth.getSession();
    if (error) throw error;
    cachedSession = data.session || null;
    cachedUser = cachedSession ? cachedSession.user : null;
    return cachedSession;
  }

  function isLoggedIn() {
    return Boolean(cachedSession);
  }

  function getUsername() {
    return cachedUser ? cachedUser.email : "";
  }

  async function register(email, password) {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });
    if (error) throw error;
    cachedSession = data.session || null;
    cachedUser = data.user || null;
    return { email: cachedUser ? cachedUser.email : email };
  }

  async function login(email, password) {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    if (error) throw error;
    cachedSession = data.session || null;
    cachedUser = data.user || null;
    return { email: cachedUser ? cachedUser.email : email };
  }

  async function logout() {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
    cachedSession = null;
    cachedUser = null;
  }

  async function resetPassword(email) {
    const { error } = await supabase.auth.resetPasswordForEmail(email);
    if (error) throw error;
    return { ok: true };
  }

  async function getUserId() {
    if (cachedUser) return cachedUser.id;
    const { data, error } = await supabase.auth.getUser();
    if (error) throw error;
    cachedUser = data.user || null;
    return cachedUser ? cachedUser.id : null;
  }

  async function getWorkout(key) {
    const { data, error } = await supabase
      .from("workouts")
      .select("data, updated_at")
      .eq("workout_key", key)
      .maybeSingle();
    if (error) throw error;
    if (!data) return null;
    return { data: data.data, updated_at: data.updated_at };
  }

  async function saveWorkout(key, data) {
    const userId = await getUserId();
    if (!userId) throw new Error("Not signed in");
    const payload = {
      user_id: userId,
      workout_key: key,
      data,
      updated_at: new Date().toISOString(),
    };
    const { error } = await supabase
      .from("workouts")
      .upsert(payload, { onConflict: "user_id,workout_key" });
    if (error) throw error;
    return { ok: true };
  }

  window.AuthClient = {
    init,
    isLoggedIn,
    getUsername,
    register,
    login,
    logout,
    resetPassword,
    getWorkout,
    saveWorkout,
  };
})();
