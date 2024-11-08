<script>
	import { onMount } from 'svelte';
	import { BASE_URL } from '../searchengine.js';
	import { selectedImageStore, queryStore } from '../searchQueryStore.js';
	import { getJson } from '../util.js';

	let selectedImage = null;

	let MAPR_CONFIG_BY_NS = {};

	let annotations = [];

	onMount(() => {
		let maprConigUrl = `${BASE_URL}mapr/api/config/`;
		getJson(maprConigUrl).then((data) => {
			var ns2menu = {};
			Object.entries(data).forEach(([key, obj]) => {
				ns2menu[obj.ns] = obj;
			});
			console.log('ns2menu', ns2menu);
			MAPR_CONFIG_BY_NS = ns2menu;
		});
	});

	selectedImageStore.subscribe((image) => {
		selectedImage = image;
		annotations = [];
		loadImage(image);
	});

	async function loadImage(image) {
    if (!image) {
      return;
    }
		let url = `${BASE_URL}webclient/api/annotations/?type=map&image=${image.id}`;
		let data = await getJson(url);
		console.log('Annotations', data);
		annotations = data.annotations;
	}
</script>

{#if selectedImage}
		<div class="details">
			<h3>{selectedImage.name}</h3>
			<h4>
        Image ID: {selectedImage.id}
        <a class="viewer_link" href="{BASE_URL}webclient/img_detail/{selectedImage.id}" target="_blank">
          Full Viewer
        </a>
      </h4>
		</div>

		<div class="scrollable">
			<div class="annotations">
				{#each annotations as ann}
					<div class="map_ann">
						<table>
							<thead>
								<tr title="${ann.ns}">
									<th colspan="2"><h2>{MAPR_CONFIG_BY_NS[ann.ns]?.label || ann.ns}</h2></th>
								</tr>
							</thead>
							<tbody>
								{#each ann.values as v}
									<tr class="tablerow">
										<td>{v[0]}</td>
										<td>
                      <!-- Link to this image with filter by KVP: ?key=Gene+Symbol&value=pax7&operator=equals -->
                      <!-- but actual link click just adds filter -->
                      <a class="kvp_link"
                        on:click|preventDefault={() => queryStore.addFilter({ key: v[0], value: v[1], dtype: "image", operator: "equals" })}
                         title="Filter by this key-value pair"
                         href="{window.location.origin + window.location.pathname}?key={v[0]}&value={v[1]}&operator=equals&show=image-{selectedImage.id}">
                        {v[1]}
                      </a>
                    </td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				{/each}
			</div>
		</div>
{/if}

<style>

  .viewer_link {
    border: solid #aaa 1px;
    display: block;
    border-radius: 5px;
    text-decoration: none;
    padding: 1px 3px;
    float: right;
    font-size: 13px;
    color: inherit;
  }
  .kvp_link {
    color: inherit;
    text-decoration: none;
  }
  .kvp_link:hover {
    text-decoration: underline;
  }
  a:visited {
    color: inherit;
  }
  .details {
    flex: auto 0 0;
    padding-bottom: 10px;
  }
  .scrollable {
    flex: auto 1 1;
    overflow: auto;
  }
	.annotations {
		color: hsl(210, 10%, 30%);
		font-size: 12px;
		background-color: hsl(220, 20%, 95%);
		display: flex;
		flex-direction: column;
		z-index: 0;
		height: 100px;
	}
	.annotations table {
		width: 100%;
	}
	.annotations h2 {
		font-size: 16px;
		color: hsl(210, 10%, 30%);
		inset: 0;
		flex: auto 0 0;
		margin: 10px;
		text-align: left;
	}
	.annotations th h2 {
		font-size: 15px;
		margin: 0;
	}

	.tablerow {
		background: hsl(220, 20%, 95%);
		border: solid #ddd 1px;
	}
	.map_ann td,
	.map_ann th {
		padding: 2px;
		background-color: hsl(220, 20%, 95%);
		width: 50%;
		max-width: 100px;
		overflow-wrap: break-word;
		overflow: hidden;
	}
	.map_ann {
		padding: 0;
		margin: 0;
	}
	.map_ann table {
		margin: 0;
		border-collapse: collapse;
	}
</style>
