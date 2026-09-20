module.exports = (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify({ status: 'OK', nodeVersion: process.version, envUrl: Boolean(process.env.SUPABASE_URL) }));
};
