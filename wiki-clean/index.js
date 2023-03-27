import bodyParser from "body-parser";
import cors from "cors";
import express from "express";

import clean from "./src/clean.js";
import getNormalArticle from "./src/getArticle.js";

const app = express();
app.use(bodyParser.json({ limit: "50mb" }));
app.use(cors());

app.use((req, _, next) => {
  console.log("Request: ", req.method, req.url);
  next();
});

app.get("/", (req, res) => {
  res.send("Hello World!");
});

app.post("/clean", (req, res, next) => {
  try {
    const { text } = req.body;

    const cleanText = clean(text);
    res.json({ text: cleanText });
  } catch (e) {
    next(e);
  }
});

app.post("/article", (req, res, next) => {
  try {
    const { title } = req.body;
    console.log("title", title);
    return getNormalArticle(title)
      .then((text) => {
        res.json({ text });
      })
      .catch((e) => {
        next(e);
      });
  } catch (e) {
    next(e);
  }
});

const port = 6000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
