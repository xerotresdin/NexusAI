const express = require("express");
const bodyParser = require("body-parser");
const { exec } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();
const port = 3000;

const multer = require("multer");
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.post("/analysis", upload.single("file"), (req, res) => {
  const data = req.file;
  if (!data) {
    return res.status(400).json({ error: "No file uploaded" });
  }

  const pythonScriptPath = path.join(__dirname, "./python/CreateGraph.py");
  const command = `python3 ${pythonScriptPath} "${data.originalname}"`;

  exec(command, (err, stdout, stderr) => {
    if (err) {
      console.error(`Error: ${err.message}`);
      return res.status(500).send("Internal Server Error");
    }

    res.send(stdout);
  });

  const imagePath = path.join(__dirname, "../graph.png");
  const imageContent = fs.readFileSync(imagePath);

  if (!res.headersSent) {
    res.setHeader("Content-Type", "image/png");
    res.send(imageContent);
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
