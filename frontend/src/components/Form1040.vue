<template>
    <div class="relative" style="width: 856px; height: 1476px">
        <img
            src="../assets/1040combined.jpg"
            style="position:absolute; top:0;"
        />

        <!-- Filing Status -->
        <img
            v-if="dummy === 'Single'"
            class="check"
            src="../assets/check.png"
            style="top:90px; left: 132px;"
        />
        <img
            v-if="dummy === 'MFJ'"
            class="check"
            src="../assets/check.png"
            style="top:90px; left: 192px;"
        />
        <img
            v-if="dummy === 'MFS'"
            class="check"
            src="../assets/check.png"
            style="top:90px; left: 311px;"
        />
        <img
            v-if="dummy === 'HOH'"
            class="check"
            src="../assets/check.png"
            style="top:90px; left: 470px;"
        />
        <img
            v-if="dummy === 'QW'"
            class="check"
            src="../assets/check.png"
            style="top:90px; left: 609px;"
        />

        <!-- User Info -->
        <input
            class="absolute formField"
            v-model="params['given-name']"
            style="top: 153px; left: 54px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="params['last-name']"
            style="top: 153px; left: 332px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 219px; left: 584px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="params['street-address']"
            style="top: 219px; left: 54px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="cityState"
            style="top: 253px; left: 54px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="params['social_security']"
            style="top: 153px; left: 652px;"
            size="50"
            disabled
        />

        <!-- User Spouse Info -->
        <input
            class="formField"
            v-model="dummy"
            style="top: 186px; left: 54px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 186px; left: 332px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 186px; left: 652px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 186px; left: 696px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            v-model="dummy"
            style="top: 186px; left: 728px;"
            size="50"
            disabled
        />

        <!-- Foreign Country Info -->
        <input
            class="formField"
            style="top: 285px; left: 54px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 285px; left: 362px;"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 285px; left: 561px;"
            size="50"
            disabled
        />

        <!-- Dependent Info -->
        <input
            class="formField"
            style="top: 396px; left: 55px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 396px; left: 227px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 396px; left: 342px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 396px; left: 378px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 396px; left: 405px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 396px; left: 465px; font-size: 14px"
            size="50"
            disabled
        />

        <input
            class="formField"
            style="top: 413px; left: 55px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 413px; left: 227px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 413px; left: 342px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 413px; left: 378px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 413px; left: 405px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 413px; left: 465px; font-size: 14px"
            size="50"
            disabled
        />

        <input
            class="formField"
            style="top: 430px; left: 55px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 430px; left: 227px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 430px; left: 342px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 430px; left: 378px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 430px; left: 405px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 430px; left: 465px; font-size: 14px"
            size="50"
            disabled
        />

        <input
            class="formField"
            style="top: 447px; left: 55px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 447px; left: 227px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 447px; left: 342px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 447px; left: 378px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 447px; left: 405px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 447px; left: 465px; font-size: 14px"
            size="50"
            disabled
        />

        <!-- Money Info -->
        <input
            class="formField"
            style="top: 463px; left: 700px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 479px; left: 700px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 496px; left: 700px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 513px; left: 700px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 529px; left: 700px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 547px; left: 700px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 563px; left: 700px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 579px; left: 700px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 596px; left: 700px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 613px; left: 700px; font-size: 14px"
            size="50"
            disabled
        />
        <input
            class="formField"
            style="top: 629px; left: 700px; font-size: 14px"
            size="50"
            disabled
        />
        <!-- Don't touch this - this is a crucical hack -->
        <input class="hidden" v-model="dirtyBit"/>
    </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "Form1040",
  computed: {
    cityState: function() {
      const city = this.params["city"];
      const state = this.params["state"];
      if (city && state) {
        return city + " " + state;
      }
      if (city) {
        return city;
      }
      if (state) {
        return state;
      }
      return "";
    },
    ...mapState({
      params: state => state.formData,
      dirtyBit: state => state.dirtyBit
    })
  },
  created: function() {
    const fields = [
      "age",
      "capital-gains",
      "city",
      "given-name",
      "is-married",
      "last-name",
      "num_dependents",
      "occupation",
      "owns-business",
      "pensions-annuities",
      "social_security",
      "ss-benefits",
      "state",
      "street-address",
      "wages",
      "zip-code"
    ];
    const dummyObj = {};
    for (const field of fields) {
      dummyObj[field] = null;
    }
    this.$store.dispatch("updateForm1040", dummyObj);
  },
  data() {
    return {
      dummy: ""
    };
  }
};
</script>

<style scoped>
.formField {
  position: absolute;
  background-color: rgba(0, 0, 0, 0);
  line-height: 3px;
  color: red;
}

.check {
  position: absolute;
  width: 15px;
}
</style>