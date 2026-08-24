(() => {
  const storageKey = "paper-index-sort";
  const collator = new Intl.Collator(["zh-CN", "en"], {
    numeric: true,
    sensitivity: "base",
  });

  function initPaperIndexSort() {
    const toolbar = document.querySelector("[data-paper-index-toolbar]");
    const select = document.querySelector("#paper-index-sort");
    const tbody = document.querySelector("#paper-index-table tbody");
    if (!toolbar || !select || !tbody || toolbar.dataset.ready === "true") return;

    toolbar.dataset.ready = "true";
    const rows = Array.from(tbody.querySelectorAll("tr"));
    const saved = window.localStorage.getItem(storageKey);
    if (saved && Array.from(select.options).some((option) => option.value === saved)) {
      select.value = saved;
    }

    const value = (row, index) => row.cells[index]?.textContent.trim() || "";
    const comparators = {
      "added-desc": (a, b) => value(b, 1).localeCompare(value(a, 1)) || collator.compare(value(a, 0), value(b, 0)),
      "added-asc": (a, b) => value(a, 1).localeCompare(value(b, 1)) || collator.compare(value(a, 0), value(b, 0)),
      "year-desc": (a, b) => Number.parseInt(value(b, 2), 10) - Number.parseInt(value(a, 2), 10) || collator.compare(value(a, 0), value(b, 0)),
      "title-asc": (a, b) => collator.compare(value(a, 0), value(b, 0)),
    };

    const sortRows = () => {
      rows.sort(comparators[select.value] || comparators["added-desc"]);
      rows.forEach((row) => tbody.appendChild(row));
      window.localStorage.setItem(storageKey, select.value);
    };

    select.addEventListener("change", sortRows);
    sortRows();
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(initPaperIndexSort);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initPaperIndexSort);
  } else {
    initPaperIndexSort();
  }
})();
