<script>
  import Fa from 'svelte-fa';
  import { faTrash } from '@fortawesome/free-solid-svg-icons';
  import form_select_bg_img from "../lib/assets/selectCaret.svg";
  import { groupStore } from '../groupQueryStore';

  export let keys = [];

  let groupby_option = "-";
  let groups = [];

  groupStore.subscribeGroups((newGroups) => {
    console.log('CentrePanelGroups.svelte -> groups', newGroups);
    groups = newGroups;
  });

  function handleKeyChoice(event) {
    let key = event.target.value;
    groupStore.addGroup(key);
    // reset <select>
    groupby_option = "-";
  }
</script>

<select bind:value={groupby_option} onchange={handleKeyChoice} style="--form-select-bg-img: url('{form_select_bg_img}')">
  <option value="-">Group by...</option>
  {#each keys as key}
    <option value={key} disabled={groups.includes(key)}>
      {key}
    </option>
  {/each}
</select>

<div class="groups_list">
  {#each groups as group, idx}
    {#if idx > 0} &gt; {/if}
    <button onclick={() => groupStore.removeGroup(idx)} title="Remove 'Group by'">
      {group}
      <span class="delete"><Fa icon={faTrash} color="#666" /></span>
    </button>
  {/each}
</div>

<style>
  button {
    border: solid grey 1px;
    padding: 0 5px 0 15px;
    margin: 5px 5px 4px 5px;
    border-radius: 5px;
    font-size: 15px;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 5px;
  }
  button .delete {
    visibility: hidden;
  }
  button:hover .delete {
    visibility: visible;
  }

  select {
    display: block;
    width: 130px;
    padding: 3px 36px 3px 10px;
    font-size: 14px;
    line-height: 1.5;
    appearance: none;
    background-color: #333333;
    color: white;
    border: 1px solid 333333;
    border-radius: 0.375rem;
    margin: 3px;
    float: left;
    background-image: var(--form-select-bg-img);
    background-repeat: no-repeat;
    background-position: right 0.75rem center;
    background-size: 16px 12px;
  }
  .groups_list {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 5px;
    align-items: center;
  }
</style>
