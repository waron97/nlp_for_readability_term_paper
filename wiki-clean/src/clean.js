import wtf from "wtf_wikipedia";

const clean = (wikitext) => {
  return wtf(wikitext).text();
};

export default clean;
