const messageInput =
    document.getElementById("message");

const equipmentSelect =
    document.getElementById("equipment");

const photoInput =
    document.getElementById("photo");

const fileName =
    document.getElementById("fileName");

const sendButton =
    document.getElementById("sendButton");

const chatMessages =
    document.getElementById("chatMessages");

const imagePreviewContainer =
    document.getElementById("imagePreviewContainer");

const imagePreview =
    document.getElementById("imagePreview");

const removeImageButton =
    document.getElementById("removeImage");

const quickCards =
    document.querySelectorAll(".quick-card");


// =========================================================
// QUICK EQUIPMENT SELECTION
// =========================================================

quickCards.forEach((card) => {

    card.addEventListener("click", () => {

        const equipment =
            card.dataset.equipment;

        equipmentSelect.value =
            equipment;

        messageInput.focus();

    });

});


// =========================================================
// IMAGE PREVIEW
// =========================================================

photoInput.addEventListener("change", () => {

    if (!photoInput.files.length) {

        hideImagePreview();

        return;
    }


    const file =
        photoInput.files[0];


    if (!file.type.startsWith("image/")) {

        alert("Please select an image file.");

        hideImagePreview();

        return;
    }


    if (file.size > 5 * 1024 * 1024) {

        alert("Image must be smaller than 5 MB.");

        hideImagePreview();

        return;
    }


    const reader =
        new FileReader();


    reader.onload = (event) => {

        imagePreview.src =
            event.target.result;

        imagePreviewContainer.style.display =
            "block";

        fileName.textContent =
            file.name;

    };


    reader.onerror = () => {

        alert("Could not read the selected image.");

        hideImagePreview();

    };


    reader.readAsDataURL(file);

});


removeImageButton.addEventListener(
    "click",
    hideImagePreview
);


function hideImagePreview() {

    imagePreview.src = "";

    imagePreviewContainer.style.display =
        "none";

    photoInput.value = "";

    fileName.textContent = "";

}


// =========================================================
// ENTER TO SEND
// =========================================================

messageInput.addEventListener("keydown", (event) => {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendMessage();

    }

});


// =========================================================
// SEND BUTTON
// =========================================================

sendButton.addEventListener(
    "click",
    sendMessage
);


// =========================================================
// SEND MESSAGE
// =========================================================

async function sendMessage() {

    const message =
        messageInput.value.trim();

    const equipment =
        equipmentSelect.value;


    if (!message) {

        messageInput.focus();

        return;
    }


    if (!equipment) {

        alert("Please select the equipment.");

        return;
    }


    // Prevent double submissions
    sendButton.disabled = true;

    sendButton.innerHTML =
        "Analyzing <span>...</span>";


    // Show user message
    addUserMessage(
        message,
        equipment
    );


    // Show loading state
    const loadingMessage =
        addLoadingMessage();


    try {

        const formData =
            new FormData();


        formData.append(
            "equipment",
            equipment
        );


        formData.append(
            "message",
            message
        );


        if (photoInput.files.length) {

            formData.append(
                "photo",
                photoInput.files[0]
            );

        }


        const response =
            await fetch(
                "/api/chat",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        loadingMessage.remove();


        if (!response.ok || !data.success) {

            throw new Error(
                data.error ||
                "NODEFIX could not process the request."
            );

        }


        addAssistantMessage(data);


    } catch (error) {

        console.error(
            "NODEFIX error:",
            error
        );


        loadingMessage.remove();


        addAssistantMessage({

            answer:
                "I couldn't process that request right now.\n\n"
                + "Please check that the Flask server is running "
                + "and try again.",

            confidence:
                "Unavailable",

            sources: [],

            escalated: false,

            ticket_id: null

        });

    } finally {

        sendButton.disabled = false;

        sendButton.innerHTML =
            'Diagnose issue <span>→</span>';


        messageInput.value = "";

        hideImagePreview();

        messageInput.focus();

    }

}


// =========================================================
// ADD USER MESSAGE
// =========================================================

function addUserMessage(
    message,
    equipment
) {

    const wrapper =
        document.createElement("div");


    wrapper.className =
        "live-message user-live-message";


    wrapper.innerHTML = `

        <div class="live-content user-content">

            <div class="live-name">
                YOU · ${escapeHtml(equipment)}
            </div>

            <div class="live-bubble user-bubble">

                ${escapeHtml(message)}

            </div>

        </div>

    `;


    chatMessages.appendChild(wrapper);

    scrollChat();

}


// =========================================================
// ADD LOADING MESSAGE
// =========================================================

function addLoadingMessage() {

    const wrapper =
        document.createElement("div");


    wrapper.className =
        "live-message";


    wrapper.innerHTML = `

        <div class="live-avatar">
            N
        </div>

        <div class="live-content">

            <div class="live-name">
                NODEFIX
            </div>

            <div class="live-bubble">

                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>

                <span style="margin-left:7px;">
                    Checking the problem...
                </span>

            </div>

        </div>

    `;


    chatMessages.appendChild(wrapper);

    scrollChat();


    return wrapper;

}


// =========================================================
// ADD AI RESPONSE
// =========================================================

function addAssistantMessage(data) {

    const wrapper =
        document.createElement("div");


    wrapper.className =
        "live-message";


    const formattedAnswer =
        escapeHtml(data.answer)
            .replaceAll(
                "\n",
                "<br>"
            );


    const sourceHTML =
        data.sources &&
        data.sources.length

            ? data.sources
                .map(
                    source =>
                        `
                        <span class="meta-pill source-pill">
                            ${escapeHtml(source)}
                        </span>
                        `
                )
                .join("")

            : "";


    let escalationHTML =
        "";


    if (data.escalated) {

        escalationHTML = `

            <div class="ticket-card">

                <div class="ticket-icon">
                    ✓
                </div>

                <div class="ticket-content">

                    <strong>
                        TECHNICIAN TICKET CREATED
                    </strong>

                    <span>
                        ${data.ticket_id
                            ? `Ticket #${escapeHtml(data.ticket_id)}`
                            : "Ticket created"}
                    </span>

                    <small>
                        ${data.escalation_reason
                            ? escapeHtml(data.escalation_reason)
                            : "Human assistance required"}
                    </small>

                </div>

                <div class="ticket-priority">
                    HUMAN REVIEW
                </div>

            </div>

        `;

    }


    wrapper.innerHTML = `

        <div class="live-avatar">
            N
        </div>


        <div class="live-content">

            <div class="live-name">
                NODEFIX AI
            </div>


            <div class="live-bubble">

                ${formattedAnswer}

            </div>


            <div class="result-meta">

                <span class="meta-pill">

                    CONFIDENCE:
                    ${escapeHtml(
                        data.confidence || "N/A"
                    )}

                </span>

                ${sourceHTML}

            </div>


            ${escalationHTML}

        </div>

    `;


    chatMessages.appendChild(wrapper);

    scrollChat();

}


// =========================================================
// SCROLL CHAT
// =========================================================

function scrollChat() {

    chatMessages.scrollTo({

        top:
            chatMessages.scrollHeight,

        behavior:
            "smooth"

    });

}


// =========================================================
// ESCAPE HTML
// =========================================================

function escapeHtml(value) {

    return String(value)

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );

}