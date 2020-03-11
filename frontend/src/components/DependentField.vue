<template>
    <div>
        <input
            class="formField"
            v-model="dependents[depIndex]['given-name']"
            style="left: 55px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dependents[depIndex]['last-name']"
            style="left: 227px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="socialSecurity"
            style="left: 342px; font-size: 14px"
            size="50"
            disabled
        />

        <input
            class="formField"
            v-model="dependents[depIndex]['relationship_to_filer']"
            style="left: 465px; font-size: 14px"
            size="50"
            disabled
        />
        <img
            v-if="false"
            class="check"
            src="@/assets/check.png"
            style="left: 633px;"
        />
        <img
            v-if="false"
            class="check"
            src="@/assets/check.png"
            style="left: 744px;"
        />
    </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "DependentField",
  props: ["depIndex"],
  computed: {
    socialSecurity: function() {
      const db = this.dirtyBit; //hack
      if (!this.dependents[this.depIndex]["social_security"]) return "";
      let str = "";
      for (let i = 0; i < 9; i++) {
        str += this.dependents[this.depIndex]["social_security"][i] + " ";
      }
      str = str.slice(0, 5) + " " + str.slice(5, 9) + " " + str.slice(9);
      return str;
    },
    ...mapState({
      dependents: state => state.document.dependents,
      dirtyBit: state => state.document.dirtyBit
    })
  },
  data() {
    return {
      dummy: null
    };
  }
};
</script>
<style scoped>
.formField {
  position: absolute;
  background-color: rgba(187, 33, 33, 0);
  line-height: 3px;
  color: red;
}

.check {
  position: absolute;
  width: 15px;
}
</style>