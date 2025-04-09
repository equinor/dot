/* eslint-disable no-console */
import express from "express";
import rateLimit from "express-rate-limit";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const app = express();
const router = express.Router();
const __dirname = dirname(fileURLToPath(import.meta.url));
const path = __dirname + "/";
const port = 3000;

const limiter = rateLimit({
  windowMs: 60 * 1000,
  max: 100,
});

app.set("trust proxy", 1);

app.use(limiter);

// Define routes
router.get("*", (req, res) => {
  res.sendFile(path + "build/index.html");
});

app.use(express.static(path + "build/"));
app.use("/", router);

app.listen(port, () => {
  console.log(`Dot is running on port ${port}`);
});
