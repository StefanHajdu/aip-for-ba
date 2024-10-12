<script lang="ts">
  export let answer;
</script>

<div class="grid gap-4">
  <div class="flex items-start gap-2.5 pl-2">
    <div
      class="leading-1.5 flex w-full max-w-[320px] flex-col rounded-r-xl rounded-bl-xl border-gray-200 bg-gray-200 p-4 dark:bg-gray-700"
    >
      <div class="flex items-center space-x-2 rtl:space-x-reverse">
        <span class="text-sm font-semibold text-gray-900 dark:text-white"
          >Bot</span
        >
        <span class="text-sm font-normal text-gray-500 dark:text-gray-400"
          >11:46</span
        >
      </div>
      <p class="py-2.5 text-sm font-normal text-gray-900 dark:text-white">
        {answer}
      </p>
    </div>
  </div>
</div>
