import sqlite3 from "sqlite3";
import wtf from "wtf_wikipedia";

const clean = (wikitext) => {
  return wtf(wikitext).text();
};

const main = async () => {
  const db = new sqlite3.Database("../data/data.db");
  db.serialize(() => {
    db.each("SELECT id, text, title FROM simple_wiki", (err, row) => {
      const { id, text, title } = row;
      let cleanText = "";
      try {
        cleanText = clean(text);
      } catch {
        console.log("[ERROR] " + title);
      }
      db.run(
        "UPDATE simple_wiki SET text_clean = ? WHERE id = ?",
        [cleanText, id],
        (err) => {
          if (err) {
            console.log("[ERROR]", err);
          } else {
            console.log(`Updated ${title}`);
          }
        }
      );
    });
  });
};

main();
