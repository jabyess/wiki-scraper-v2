console.log("script loaded");

const init = () => {
  const form = document.querySelector("form");
  // const inputString
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    console.log("submitted");

    const inputField = document.querySelector("input");
    console.log(inputField.value);

    try {
      const res = await fetch(`/crawl`, {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        },
        body: JSON.stringify({
          url: encodeURI(inputField.value)
        }),
      });
      const json = await res.json();
      console.log(json);
    } catch (err) {
      console.error(err);
    }
  });
};

document.addEventListener("DOMContentLoaded", init);
