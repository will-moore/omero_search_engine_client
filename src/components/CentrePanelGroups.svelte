<script>
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
    <option value={key}>{key}</option>
  {/each}
</select>

<div>
  {#each groups as group, idx}
    {#if idx > 0} &gt; {/if}
    <span>{group}</span>
  {/each}
</div>

<style>
  span {
    border: solid grey 1px;
    padding: 0 5px;
    margin: 5px;
    border-radius: 5px;
    display: inline-block;
    font-size: 15px;
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
</style>
