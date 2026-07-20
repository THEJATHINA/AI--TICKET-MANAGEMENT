// Get Elements (preserve IDs used by other modules / future API integrations)
const ticketBody = document.getElementById("ticketBody");
const searchInput = document.getElementById("searchInput");
const loadingState = document.getElementById("loadingState");
const emptyState = document.getElementById("emptyState");

const modal = document.getElementById("detailsModal");
const details = document.getElementById("ticketDetails");
const closeBtn = document.querySelector(".close-btn");

// Summary card elements
const totalTicketsEl = document.getElementById("totalTickets");
const openTicketsEl = document.getElementById("openTickets");
const closedTicketsEl = document.getElementById("closedTickets");
const highTicketsEl = document.getElementById("highTickets");
const mediumTicketsEl = document.getElementById("mediumTickets");
const lowTicketsEl = document.getElementById("lowTickets");

const API_BASE_URL = "http://127.0.0.1:8001/api/tickets";
const CLASSIFICATION_API_URL = "http://127.0.0.1:8000/classify";

let currentTickets = [];

function escapeHtml(value) {
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

function severityBadge(sev) {
    const s = String(sev || "").toLowerCase();
    if (s.includes("high") || s.includes("critical")) return `<span class="badge high">High</span>`;
    if (s.includes("medium")) return `<span class="badge medium">Medium</span>`;
    return `<span class="badge low">Low</span>`;
}

function statusBadge(st) {
    const s = String(st || "").toLowerCase();
    if (s.includes("closed") || s.includes("resolved")) return `<span class="status classified">Closed</span>`;
    if (s.includes("in_progress") || s.includes("open")) return `<span class="status pending">Open</span>`;
    return `<span class="status failed">Pending</span>`;
}

function confidenceHTML(score) {
    let pct = 0;
    if (typeof score === "string" && score.includes("%")) {
        pct = parseInt(score, 10);
    } else {
        pct = Number(score) || 0;
    }

    if (pct > 1) {
        pct = pct > 100 ? 100 : pct;
    } else {
        pct = Math.max(0, Math.min(100, pct * 100));
    }

    return `
        <div class="progress" aria-valuenow="${pct}" aria-valuemin="0" aria-valuemax="100">
            <div class="progress-bar" style="width:${pct}%"></div>
        </div>
        <div style="font-size:12px;margin-top:6px;color:var(--muted)">${pct.toFixed(0)}%</div>
    `;
}

function formatValue(value, fallback = "—") {
    if (value === null || value === undefined || value === "") {
        return fallback;
    }
    return value;
}

function formatConfidence(value) {
    if (value === null || value === undefined || value === "") {
        return "—";
    }

    const numeric = Number(value);
    if (Number.isNaN(numeric)) {
        return String(value);
    }

    const pct = numeric > 1 ? numeric : numeric * 100;
    return `${Math.max(0, Math.min(100, pct)).toFixed(0)}%`;
}

function normalizeTicket(ticket) {
    const department = ticket.department || ticket.category || ticket.classification || "Pending";
    const confidence = ticket.confidence ?? ticket.confidence_score ?? null;

    return {
        ticket_id: ticket.ticket_id ?? ticket.id,
        subject: ticket.subject || "Untitled Ticket",
        description: ticket.description || "",
        department,
        category: ticket.category || department,
        severity: ticket.severity || "Low",
        priority: ticket.priority || "P4",
        confidence,
        status: ticket.status || "Open",
        created_at: ticket.created_at || "",
    };
}

function setEmptyState(title, message) {
    if (!emptyState) return;

    emptyState.hidden = false;
    const titleEl = emptyState.querySelector("h3");
    const messageEl = emptyState.querySelector("p");

    if (titleEl) titleEl.textContent = title;
    if (messageEl) messageEl.textContent = message;
}

function renderTickets(ticketList) {
    if (ticketBody) {
        ticketBody.innerHTML = "";
    }

    if (!ticketList || ticketList.length === 0) {
        if (emptyState) emptyState.hidden = false;
        if (loadingState) loadingState.hidden = true;
        setEmptyState("No tickets found", "Try a different keyword or refresh the page to load new data.");
        return;
    }

    if (emptyState) emptyState.hidden = true;
    if (loadingState) loadingState.hidden = true;

    ticketList.forEach((ticket) => {
        const normalized = normalizeTicket(ticket);
        const severity = severityBadge(normalized.severity);
        const status = statusBadge(normalized.status);
        const confidence = confidenceHTML(normalized.confidence);

        ticketBody.innerHTML += `
            <tr>
                <td>${escapeHtml(normalized.ticket_id)}</td>
                <td style="text-align:left;padding-left:18px">${escapeHtml(normalized.subject)}</td>
                <td>${escapeHtml(normalized.department)}</td>
                <td>${severity}</td>
                <td>${escapeHtml(normalized.priority)}</td>
                <td>${confidence}</td>
                <td>${status}</td>
                <td>
                    <button class="view-btn" onclick="viewTicket('${normalized.ticket_id}')" aria-label="View ${escapeHtml(normalized.ticket_id)}">
                        <i class="fa-solid fa-eye"></i>
                        View
                    </button>
                </td>
            </tr>
        `;
    });

    const bars = document.querySelectorAll(".progress-bar");
    bars.forEach((bar) => {
        const w = bar.style.width;
        bar.style.width = "0%";
        setTimeout(() => {
            bar.style.width = w;
        }, 30);
    });
}

function updateSummaries(list) {
    const total = list.length;
    const open = list.filter((ticket) => String(ticket.status || "").toLowerCase().includes("open") || String(ticket.status || "").toLowerCase().includes("in_progress")).length;
    const closed = total - open;
    const high = list.filter((ticket) => String(ticket.severity || "").toLowerCase().includes("high") || String(ticket.severity || "").toLowerCase().includes("critical")).length;
    const medium = list.filter((ticket) => String(ticket.severity || "").toLowerCase().includes("medium")).length;
    const low = list.filter((ticket) => String(ticket.severity || "").toLowerCase().includes("low")).length;

    if (totalTicketsEl) totalTicketsEl.textContent = total;
    if (openTicketsEl) openTicketsEl.textContent = open;
    if (closedTicketsEl) closedTicketsEl.textContent = closed;
    if (highTicketsEl) highTicketsEl.textContent = high;
    if (mediumTicketsEl) mediumTicketsEl.textContent = medium;
    if (lowTicketsEl) lowTicketsEl.textContent = low;
}

async function getClassificationForTicket(description) {
    if (!description) {
        return { department: "Pending", confidence: null };
    }

    try {
        const response = await fetch(CLASSIFICATION_API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: description }),
        });

        if (!response.ok) {
            throw new Error("Classification endpoint unavailable");
        }

        const payload = await response.json();
        return {
            department: payload.department || payload.category || "Pending",
            confidence: payload.confidence ?? null,
        };
    } catch (error) {
        console.warn("Classification API unavailable, using fallback values:", error);
        return { department: "Pending", confidence: null };
    }
}

async function loadTicketsFromApi() {
    if (loadingState) loadingState.hidden = false;
    if (emptyState) emptyState.hidden = true;

    try {
        const response = await fetch(API_BASE_URL);
        if (!response.ok) {
            throw new Error("Unable to fetch tickets");
        }

        const data = await response.json();
        currentTickets = Array.isArray(data) ? data.map(normalizeTicket) : [];
        renderTickets(currentTickets);
        updateSummaries(currentTickets);
    } catch (error) {
        console.warn("Backend not reachable, showing empty state:", error);
        currentTickets = [];
        renderTickets([]);
        updateSummaries([]);
        setEmptyState("Unable to load tickets", "The ticket service is unavailable right now. Please try again shortly.");
    }
}

async function viewTicket(id) {
    const ticket = currentTickets.find((item) => String(item.ticket_id) === String(id));
    if (!ticket) return;

    details.innerHTML = `
        <div class="loading-state" role="status" aria-live="polite">
            <div class="spinner"></div>
            <p>Loading ticket details…</p>
        </div>
    `;

    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("modal-open");

    try {
        const response = await fetch(`${API_BASE_URL}/${id}`);
        if (!response.ok) {
            throw new Error("Unable to load ticket details");
        }

        const payload = await response.json();
        const normalized = normalizeTicket(payload);
        const classification = await getClassificationForTicket(normalized.description);

        if (!normalized.department || normalized.department === "Pending") {
            normalized.department = classification.department;
        }
        if (normalized.confidence === null || normalized.confidence === undefined) {
            normalized.confidence = classification.confidence;
        }

        details.innerHTML = `
            <div class="detail-row"><div class="detail-icon"><i class="fa-solid fa-hashtag"></i></div><div><div class="detail-label">Ticket ID</div><div class="detail-value">${escapeHtml(formatValue(normalized.ticket_id))}</div></div></div>
            <div class="detail-row"><div class="detail-icon"><i class="fa-solid fa-heading"></i></div><div><div class="detail-label">Subject</div><div class="detail-value">${escapeHtml(formatValue(normalized.subject))}</div></div></div>
            <div class="detail-row"><div class="detail-icon"><i class="fa-solid fa-align-left"></i></div><div><div class="detail-label">Description</div><div class="detail-value">${escapeHtml(formatValue(normalized.description))}</div></div></div>
            <div class="detail-row"><div class="detail-icon"><i class="fa-solid fa-tags"></i></div><div><div class="detail-label">Department</div><div class="detail-value">${escapeHtml(formatValue(normalized.department))}</div></div></div>
            <div class="detail-row"><div class="detail-icon"><i class="fa-solid fa-triangle-exclamation"></i></div><div><div class="detail-label">Severity</div><div class="detail-value">${escapeHtml(formatValue(normalized.severity))}</div></div></div>
            <div class="detail-row"><div class="detail-icon"><i class="fa-solid fa-flag"></i></div><div><div class="detail-label">Priority</div><div class="detail-value">${escapeHtml(formatValue(normalized.priority))}</div></div></div>
            <div class="detail-row"><div class="detail-icon"><i class="fa-solid fa-percent"></i></div><div><div class="detail-label">Confidence</div><div class="detail-value">${escapeHtml(formatConfidence(normalized.confidence))}</div></div></div>
            <div class="detail-row"><div class="detail-icon"><i class="fa-solid fa-circle-check"></i></div><div><div class="detail-label">Status</div><div class="detail-value">${escapeHtml(formatValue(normalized.status))}</div></div></div>
            <div class="detail-row"><div class="detail-icon"><i class="fa-solid fa-calendar-days"></i></div><div><div class="detail-label">Created At</div><div class="detail-value">${escapeHtml(formatValue(normalized.created_at))}</div></div></div>
        `;
    } catch (error) {
        console.warn("Unable to load ticket details:", error);
        details.innerHTML = `
            <div class="detail-row"><div class="detail-icon"><i class="fa-solid fa-triangle-exclamation"></i></div><div><div class="detail-label">Error</div><div class="detail-value">The ticket details could not be loaded right now.</div></div></div>
        `;
    }
}

function closeModal() {
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("modal-open");
}

if (closeBtn) {
    closeBtn.onclick = closeModal;
}

window.addEventListener("click", (event) => {
    if (event.target === modal) {
        closeModal();
    }
});

window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeModal();
});

window.addEventListener("DOMContentLoaded", () => {
    if (searchInput) {
        searchInput.addEventListener("keyup", () => {
            const value = searchInput.value.trim().toLowerCase();
            const filteredTickets = currentTickets.filter((ticket) => {
                const normalized = normalizeTicket(ticket);
                return String(normalized.ticket_id).toLowerCase().includes(value) ||
                    normalized.subject.toLowerCase().includes(value) ||
                    normalized.department.toLowerCase().includes(value) ||
                    normalized.status.toLowerCase().includes(value);
            });

            renderTickets(filteredTickets);
            updateSummaries(filteredTickets);
        });
    }

    loadTicketsFromApi();
});
