<script lang="ts">
  import BotA from "./BotA.svelte";
  import UserQ from "./UserQ.svelte";

  const urlStream =
    "https://aip-api.shs-net.org/generate-rag?limit=2&stream=True&model=llama3%2E1";

  const urlGenerate =
    "https://aip-api.shs-net.org/generate-rag?limit=2&stream=False&model=llama3%2E1";

  $: prompt = "";
  $: answer = "";
  $: awaitingAnswer = false;
  $: chatBubbles = [
    { id: 1, role: "bot", text: "Welcome from bot!" },
    { id: 2, role: "user", text: "User Q" },
    { id: 3, role: "bot", text: "Bot A" },
  ];
  $: numOfchatBubbles = chatBubbles.length;

  async function processInput(): Promise<void> {
    if (prompt === "") {
      return;
    }
    console.log(`from ChatDialog; run with prompt: ${prompt}`);
    awaitingAnswer = true;
    // choose answer output method
    await readOllamaAnswerGenerate();
    chatBubbles = [
      ...chatBubbles,
      { id: numOfchatBubbles + 1, role: "user", text: prompt },
      { id: numOfchatBubbles + 2, role: "bot", text: answer },
    ];
    answer = "";
    prompt = "";
    awaitingAnswer = false;
  }

  async function readOllamaAnswerStream(): Promise<void> {
    const response = await fetch(urlStream, {
      method: "POST",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
      },
      body: JSON.stringify({
        prompt: prompt,
      }),
    });

    if (response && response.body) {
      const decodedStream = response.body.pipeThrough(new TextDecoderStream());

      for await (const chunk of decodedStream) {
        let ollamaResponseObjects = [];
        try {
          ollamaResponseObjects = [JSON.parse(chunk)];
        } catch {
          // ollama sometimes stack json-like string together, which create JSON unparsable string
          const chunks = chunk.split("\n").slice(0, -1);
          ollamaResponseObjects = chunks.map((c) => {
            console.log(JSON.parse(c));
            return JSON.parse(c);
          });
        }
        for (const ollamaResponseObject of ollamaResponseObjects) {
          if (ollamaResponseObject.done) {
            break;
          }
          answer += ollamaResponseObject.response;
        }
      }
    } else {
      answer = "Invalid answer";
    }
  }

  async function readOllamaAnswerGenerate(): Promise<void> {
    const response = await fetch(urlGenerate, {
      method: "POST",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
      },
      body: JSON.stringify({
        prompt: prompt,
      }),
    });

    if (response && response.body) {
      const responseJSON = await response.json();
      answer = responseJSON.llm_answer + responseJSON.sources.toString();
    } else {
      answer = "Invalid answer!";
    }
  }
</script>

<div
  class="h-72 overflow-auto p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
>
  {#if !awaitingAnswer}
    {#each chatBubbles as chatBubble}
      {#if chatBubble.role === "bot"}
        <BotA answer={chatBubble.text} />
      {:else if chatBubble.role === "user"}
        <UserQ question={chatBubble.text} />
      {/if}
    {/each}
  {:else}
    {#each chatBubbles as chatBubble}
      {#if chatBubble.role === "bot"}
        <BotA answer={chatBubble.text} />
      {:else if chatBubble.role === "user"}
        <UserQ question={chatBubble.text} />
      {/if}
    {/each}
    <UserQ question={prompt} />
    <BotA {answer} />
  {/if}
</div>

<div>
  <label for="chat" class="sr-only">Your message</label>
  <div
    class="flex items-center rounded-lg bg-gray-50 px-3 py-2 dark:bg-gray-700"
  >
    <textarea
      id="chat"
      rows="3"
      class="mx-4 block w-full rounded-lg border border-gray-300 bg-white p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-800 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
      placeholder="Your message..."
      bind:value={prompt}
    ></textarea>
    <button
      on:click={processInput}
      class="inline-flex cursor-pointer justify-center rounded-full p-2 text-blue-600 hover:bg-blue-100 dark:text-blue-500 dark:hover:bg-gray-600"
    >
      <svg
        class="h-5 w-5 rotate-90 rtl:-rotate-90"
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        fill="currentColor"
        viewBox="0 0 18 20"
      >
        <path
          d="m17.914 18.594-8-18a1 1 0 0 0-1.828 0l-8 18a1 1 0 0 0 1.157 1.376L8 18.281V9a1 1 0 0 1 2 0v9.281l6.758 1.689a1 1 0 0 0 1.156-1.376Z"
        />
      </svg>
    </button>
  </div>
</div>
