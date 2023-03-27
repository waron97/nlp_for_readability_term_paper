import wtf from "wtf_wikipedia";

const getNormalArticle = async (title) => {
  const data = await wtf.fetch(title);
  return data.text();
};

export default getNormalArticle;
