<script setup>
import formatDate from "@/assets/utils/common/formatDate.js";
import BoolToCheckmark from "@/components/common/BoolToCheckmark.vue";
import {computed, onBeforeMount, onMounted, ref} from "vue";
import TagList from "@/components/common/TagList.vue";
import SortingArrow from "@/components/common/data_table/elements/SortingArrow.vue";
import {useUiStore} from "@/stores/ui.js";

const uiStore = useUiStore();

onBeforeMount(() => {
  if (!uiStore.tables[props.storageName]) {
    uiStore.tables[props.storageName] = {
      order: '',
      orderDirection: '',
    }
  }
});

const props = defineProps({
  storageName: {
    type: String,
    validator(value) {
      return value.length > 0;
    }
  },
  data: {
    type: Array,
    required: true,
  },
  onRowClick: {
    type: Function,
    default: (row)=>{}
  },
  structure: {
    type: Array,
    required: true,
    validator(value) {
      return value.every(item =>
        typeof item.key === 'string' &&
        typeof item.title === 'string' &&
        (typeof item.isSortable === 'undefined' || typeof item.isSortable === 'boolean' ) &&
        ['string', 'checkmark', 'date', 'tagList'].includes(item.type) // Zastąp typami, które Cię interesują
      );
    }
  }
})

const orderLocal = ref('');
const orderDirectionLocal = ref('');

const order = computed(() => {
  if (typeof(props.storageName) === "undefined"){
    return orderLocal.value;
  } else {
    try {
      return uiStore.tables[props.storageName].order;
    } catch (error) {
      return ''
    }
  }
});

const orderDirection = computed(() => {
  if (typeof(props.storageName) === "undefined"){
    return orderDirectionLocal.value;
  } else {
    try {
      return uiStore.tables[props.storageName].orderDirection;
    } catch (error) {
      return ''
    }
  }
});

const saveOrder = (value) => {
  if (typeof(props.storageName) === "undefined"){
    orderLocal.value = value;
  } else {
    uiStore.tables[props.storageName]['order'] = value;
  }
}

const saveOrderDirection = (value) => {
  if (typeof(props.storageName) === "undefined"){
    orderDirectionLocal.value = value;
  } else {
    uiStore.tables[props.storageName]['orderDirection'] = value;
  }
}

const orderedData = computed(() => {
  if (!order.value || !orderDirection.value) {
    return props.data;
  }

  return [...props.data].sort((a, b) => {
    const key = order.value;
    const direction = orderDirection.value === 'asc' ? 1 : -1;

    if (typeof a[key] === 'string' && typeof b[key] === 'string') {
      const dateA = new Date(a[key]);
      const dateB = new Date(b[key]);

      if (!isNaN(dateA.getTime()) && !isNaN(dateB.getTime())) {
        return (dateA - dateB) * direction;
      } else {
        return a[key].localeCompare(b[key]) * direction;
      }
    }
    else if (typeof a[key] === 'number' && typeof b[key] === 'number') {
      return (a[key] - b[key]) * direction;
    }
    else if (a[key] instanceof Date && b[key] instanceof Date) {
      return (a[key] - b[key]) * direction;
    }
    else if (typeof a[key] === 'boolean' && typeof b[key] === 'boolean') {
      return (a[key] === b[key] ? 0 : a[key] ? -1 : 1) * direction;
    }
    return 0;
  });
});

const setOrder = (key, isSortable) => {
  if (isSortable) {
    if (order.value === key) {
      if (orderDirection.value === 'asc') {
        saveOrderDirection('desc');
      } else if (orderDirection.value === 'desc') {
        saveOrder('')
        saveOrderDirection('');
      }
    } else {
      saveOrder(key)
      saveOrderDirection('asc');
    }
  }
}

</script>

<template>
<div class="table-container">
  <table class="table is-fullwidth is-hoverable">
    <thead>
    <tr>
      <th v-for="col in structure" @click="setOrder(col.key, col.isSortable)" :class="{'is-clickable': col.isSortable}">
        {{ col.title }}<SortingArrow v-if="col.isSortable" :active="order === col.key" :direction="orderDirection"/>
      </th>
    </tr>
    </thead>
    <tbody>
      <tr v-for="row in orderedData" class="is-clickable">
        <td v-for="col in structure" @click="onRowClick(row)">
          <span v-if="col.type === 'string'">{{ row[col.key] }}</span>
          <span v-if="col.type === 'checkmark'"><BoolToCheckmark :value="row[col.key]"/></span>
          <span v-if="col.type === 'date'">{{ formatDate(row[col.key]) }}</span>
          <span v-if="col.type === 'tagList'"><TagList :tags="row[col.key]"/></span>
        </td>
      </tr>
    </tbody>
  </table>
</div>
</template>

<style scoped>

</style>