BASE_URL = "https://tikooki-be-v2-roijbwmiyq-de.a.run.app";

//Get all recipes for main page
my.request({
  url: BASE_URL + "/get-all-recipes",
  method: "GET",
  success: (response) => {
    this.setData({ response, loading: false });
  },
});

//Get one recipe for recipe detail page
my.request({
  url: BASE_URL + "/get-recipe-by-title",
  method: "POST",
  body: {
    title: title,
    category: "unknown",
  },
  success: (response) => {
    this.setData({ response, loading: false });
  },
});
