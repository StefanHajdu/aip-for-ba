<script lang="ts">
  export let question;
</script>

<div class="flex items-start gap-2.5 pl-2">
  <div
    class="leading-1.5 flex w-full max-w-[320px] flex-col rounded-l-xl rounded-br-xl border-gray-200 bg-gray-400 p-4 dark:bg-gray-700"
  >
    <div class="flex items-center space-x-2 rtl:space-x-reverse">
      <span class="text-sm font-semibold text-gray-900 dark:text-white"
        >User</span
      >
      <span class="text-sm font-normal text-gray-500 dark:text-gray-400"
        >11:46</span
      >
    </div>
    <p class="py-2.5 text-sm font-normal text-gray-900 dark:text-white">
      {question}
    </p>
  </div>
</div>
