document.addEventListener("DOMContentLoaded", () => {
  lucide.createIcons();

  const resultsContainer = document.getElementById("results");
  const bookingCardTemplate = document.getElementById("bookingCardTemplate");

  const filtersForm = document.getElementById("filtersForm");
  const resetFiltersButton = document.getElementById("resetFilters");
  const priceRangeInput = document.getElementById("priceRange");
  const priceRangeValue = document.getElementById("priceRangeValue");

  const searchForm = document.getElementById("searchForm");
  const themeToggleButton = document.getElementById("theme-switch");

  const vehicles = [
    {
      id: "crzr-001",
      name: "Tesla Model Y Performance",
      type: "Electric",
      rating: 4.9,
      reviews: 212,
      pricePerDay: 189,
      status: "available",
      features: ["320 mi range", "Autopilot", "AWD", "Fast charging"],
      imageAlt: "Blue Tesla Model Y",
      image: ""
    },
    {
      id: "crzr-002",
      name: "BMW X5 M Sport",
      type: "SUV",
      rating: 4.8,
      reviews: 146,
      pricePerDay: 175,
      status: "available",
      features: ["Premium interior", "Heads-up display", "AWD"],
      imageAlt: "Black BMW X5",
      image: ""
    },
    {
      id: "crzr-003",
      name: "Toyota Prius Hybrid",
      type: "Sedan",
      rating: 4.7,
      reviews: 320,
      pricePerDay: 78,
      status: "available",
      features: ["Hybrid efficiency", "Smart Assist", "Apple CarPlay"],
      imageAlt: "Silver Toyota Prius",
      image: ""
    },
    {
      id: "crzr-004",
      name: "Mercedes S-Class Chauffeur",
      type: "Luxury",
      rating: 4.95,
      reviews: 98,
      pricePerDay: 240,
      status: "unavailable",
      features: ["Professional driver", "On-board Wi-Fi", "Complimentary drinks"],
      imageAlt: "Mercedes S-Class with chauffeur",
      image: ""
    },
    {
      id: "crzr-005",
      name: "Honda CR-V Comfort",
      type: "SUV",
      rating: 4.6,
      reviews: 285,
      pricePerDay: 92,
      status: "available",
      features: ["Spacious cargo", "Eco mode", "Lane Assist"],
      imageAlt: "White Honda CR-V",
      image: ""
    }
  ];

  const svgPlaceholders = {
    Electric:
      '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#0EA5E9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path></svg>',
    SUV:
      '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14l3 5v3h-2"></path><path d="M19 12l-1.5-5.5A2 2 0 0 0 15.6 5H8.4a2 2 0 0 0-1.9 1.5L5 12"></path><circle cx="7" cy="19" r="2"></circle><circle cx="17" cy="19" r="2"></circle></svg>',
    Sedan:
      '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#0EA5E9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 13l2-5h7l2 5"></path><path d="M5 18h14"></path><circle cx="7.5" cy="18" r="1.5"></circle><circle cx="16.5" cy="18" r="1.5"></circle></svg>',
    Luxury:
      '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l3-7h12l3 7"></path><path d="M5 18h14"></path><circle cx="7.5" cy="18" r="1.5"></circle><circle cx="16.5" cy="18" r="1.5"></circle><path d="M10 5h4"></path></svg>'
  };

  const renderCards = (dataset) => {
    resultsContainer.innerHTML = "";

    if (!dataset.length) {
      resultsContainer.innerHTML = `
        <div class="empty-state">
          <h3>No matches found</h3>
          <p>Adjust your filters or try a different search.</p>
        </div>`;
      lucide.createIcons();
      return;
    }

    dataset.forEach((vehicle) => {
      const node = bookingCardTemplate.content.cloneNode(true);
      const card = node.querySelector(".booking-card");

      const imageWrapper = node.querySelector(".booking-card__image-wrapper");
      const imageElement = node.querySelector(".booking-card__image");

      if (vehicle.image) {
        imageElement.src = vehicle.image;
        imageElement.alt = vehicle.imageAlt;
      } else {
        imageElement.remove();
        imageWrapper.innerHTML = svgPlaceholders[vehicle.type] || svgPlaceholders.Sedan;
      }

      node.querySelector(".booking-card__title").textContent = vehicle.name;
      node.querySelector(".booking-card__type").textContent = vehicle.type;
      node.querySelector(".booking-card__rating").textContent = `${vehicle.rating} (${vehicle.reviews})`;

      const statusBadge = node.querySelector(".badge--status");
      statusBadge.dataset.status = vehicle.status;
      statusBadge.textContent = vehicle.status === "available" ? "Available" : "Fully Booked";

      const featuresList = node.querySelector(".booking-card__features");
      vehicle.features.forEach((feature) => {
        const featureItem = document.createElement("li");
        featureItem.textContent = feature;
        featuresList.appendChild(featureItem);
      });

      node.querySelector(".booking-card__price strong").textContent = `$${vehicle.pricePerDay}`;

      const bookButton = node.querySelector(".btn--primary");
      bookButton.addEventListener("click", () => handleBooking(vehicle));

      resultsContainer.appendChild(node);
    });

    lucide.createIcons();
  };

  const handleBooking = (vehicle) => {
    if (vehicle.status !== "available") {
      alert(`${vehicle.name} is currently unavailable. Please choose another option.`);
      return;
    }

    const animatedIcon = document.createElement("div");
    animatedIcon.className = "booking-animation";
    animatedIcon.innerHTML = `
      <svg viewBox="0 0 64 32" width="64" height="32" aria-hidden="true">
        <rect x="4" y="12" width="48" height="12" rx="6" fill="url(#grad)"></rect>
        <circle cx="18" cy="26" r="6" fill="#0284C7"></circle>
        <circle cx="38" cy="26" r="6" fill="#0EA5E9"></circle>
        <defs>
          <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#0284C7;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#0EA5E9;stop-opacity:1" />
          </linearGradient>
        </defs>
      </svg>
      <span>Booking ${vehicle.name}...</span>
    `;
    document.body.appendChild(animatedIcon);

    setTimeout(() => {
      animatedIcon.classList.add("booking-animation--done", "booking-animation--success");
      animatedIcon.querySelector("span").textContent = "Booking confirmed!";
      setTimeout(() => animatedIcon.remove(), 1500);
    }, 1300);
  };

  const filterVehicles = () => {
    const formData = new FormData(filtersForm);
    const selectedTypes = formData.getAll("type");
    const maxPrice = Number(formData.get("priceRange"));
    const minRating = Number(formData.get("rating"));
    const availability = formData.get("availability");

    const filtered = vehicles.filter((vehicle) => {
      const matchesType = selectedTypes.includes(vehicle.type);
      const matchesPrice = vehicle.pricePerDay <= maxPrice;
      const matchesRating = vehicle.rating >= minRating;
      const matchesAvailability =
        availability === "all" ? true : vehicle.status === "available";

      return matchesType && matchesPrice && matchesRating && matchesAvailability;
    });

    renderCards(filtered);
  };

  priceRangeInput.addEventListener("input", (event) => {
    priceRangeValue.textContent = `$${event.target.value}`;
    filterVehicles();
  });

  filtersForm.addEventListener("change", filterVehicles);

  resetFiltersButton.addEventListener("click", () => {
    filtersForm.reset();
    filtersForm.querySelectorAll('input[type="checkbox"]').forEach((checkbox) => {
      checkbox.checked = true;
    });
    priceRangeInput.value = 150;
    priceRangeValue.textContent = "$150";
    filterVehicles();
  });

  searchForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const existingConfirmation = searchForm.nextElementSibling;
    if (existingConfirmation?.classList.contains("search-confirmation")) {
      existingConfirmation.remove();
    }

    const formData = new FormData(searchForm);
    const pickupLocation = formData.get("pickupLocation");
    const pickupDate = formData.get("pickupDate");
    const dropoffDate = formData.get("dropoffDate");

    console.table({ pickupLocation, pickupDate, dropoffDate });

    const confirmation = document.createElement("div");
    confirmation.className = "search-confirmation";
    confirmation.innerHTML = `
      <strong>Searching available rides...</strong>
      <p>${pickupLocation} | ${pickupDate} → ${dropoffDate}</p>
    `;
    searchForm.after(confirmation);

    setTimeout(() => confirmation.remove(), 2600);

    filterVehicles();
  });

  const applyTheme = (mode) => {
    const darkMode = mode === "dark";
    document.body.classList.toggle("darkmode", darkMode);
    themeToggleButton.setAttribute("aria-pressed", String(darkMode));
  };

  const savedTheme = localStorage.getItem("cruzr-theme");
  if (savedTheme) {
    applyTheme(savedTheme);
  } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    applyTheme("dark");
  }

  themeToggleButton.addEventListener("click", () => {
    const isDark = !document.body.classList.contains("darkmode");
    applyTheme(isDark ? "dark" : "light");
    localStorage.setItem("cruzr-theme", isDark ? "dark" : "light");
  });

  filterVehicles();
});