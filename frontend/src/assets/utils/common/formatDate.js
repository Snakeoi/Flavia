export default (isoDate) => {
  const date = new Date(isoDate);

  return new Intl.DateTimeFormat(navigator.language, {
    dateStyle: "short",
    timeStyle: "short"
  }).format(date);
}