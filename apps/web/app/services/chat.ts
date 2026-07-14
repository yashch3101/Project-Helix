const API = "http://127.0.0.1:8000";

export async function getSessions(
    repositoryId: string
) {

    const res = await fetch(

        `${API}/chat/sessions?repository_id=${repositoryId}`

    );

    return res.json();

}

export async function getMessages(sessionId: string) {
  const res = await fetch(`${API}/chat/${sessionId}/messages`);

  if (!res.ok) {
    throw new Error("Failed to load messages");
  }

  return res.json();
}

export async function createSession(repositoryId: string) {

  const res = await fetch(`${API}/chat/session`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      repository_id: repositoryId,
    }),
  });

  if (!res.ok) {
    throw new Error("Failed to create session");
  }

  return res.json();
}

export async function sendMessage(
  sessionId: string,
  question: string,
  signal?: AbortSignal
) {
  return fetch(`${API}/chat/message`, {
    method: "POST",

    signal,

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      session_id: sessionId,
      question,
    }),
  });
}

export async function streamMessage(
  sessionId: string,
  question: string
) {
  const response = await fetch("http://127.0.0.1:8000/chat/message", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      session_id: sessionId,
      question,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to send message");
  }

  return response;
}

export async function deleteSession(
    repositoryId: string
) {

    const res = await fetch(

        `${API}/chat/repository/${repositoryId}`,

        {

            method: "DELETE",

        }

    );

    if (!res.ok) {

        throw new Error("Failed to delete chats");

    }

    return res.json();

}

export async function deleteChat(
  sessionId: string
) {
  const res = await fetch(
    `${API}/chat/${sessionId}`,
    {
      method: "DELETE",
    }
  );

  if (!res.ok) {
    throw new Error("Failed to delete chat");
  }

  return res.json();
}

export async function renameChat(
  sessionId: string,
  title: string
) {
  const res = await fetch(
    `${API}/chat/${sessionId}/title`,
    {
      method: "PATCH",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        title,
      }),
    }
  );

  if (!res.ok) {
    throw new Error("Failed to rename chat");
  }

  return res.json();
}