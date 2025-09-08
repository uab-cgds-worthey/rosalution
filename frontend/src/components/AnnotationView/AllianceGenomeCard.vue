<template>
<div class="card-base">
  <div class="card-header" v-html="modelName" data-test="model-header"/>
  <div class="card-sub-header" v-html="modelBackground" data-test="model-background"/>
  <div class="card-content">
    <div class="card-section" :style="sectionTextColor(experimentalConditions)" data-test="model-section-condition">
        Experimental Condition
    </div>
    <ul>
      <li
        v-for="condition in experimentalConditions"
        :key="condition"
        class="card-list"
        data-test="model-list-condition"
      >
          {{ condition.conditionStatement }}
      </li>
    </ul>
    <div class="card-section" :style="sectionTextColor(diseaseModels)" data-test="model-section-disease">
      Associated Human Diseases
    </div>
    <li
      class="card-list"
      v-for="(diseaseModel) in diseaseModels" :key="diseaseModel"
      data-test="model-list-disease"
    >
      {{ diseaseModel.diseaseModel }}
    </li>
    <div class="card-section" :style="sectionTextColor(associatedPhenotypesData)" data-test="model-section-phenotype">
          Associated Phenotypes
    </div>
    <div class="card-list"
        v-for="(value, key) in associatedPhenotypesData" :key="key"
        data-test="model-list-phenotype"
    >
    <div v-if="key != ''">
        <font-awesome-icon v-if="value.icon" :icon="value.icon" :style="value.iconStyle"/>
        <span class="card-section-term" :style="value.style">{{ key }}</span>
    </div>
        <ul>
            <li v-for="item in value.phenotypes" :key="item">{{ item }}</li>
        </ul>
    </div>
    <div class="card-source" data-test="model-source">
        <b>Source:</b> {{ modelSource }}
    </div>
  </div>
</div>
</template>

<script setup>
import {computed} from 'vue';

import {chooseAnimalModelsSchema} from '@/components/AnnotationView/allianceGenomeRenderingUtility';

const props = defineProps({
  model: {
    type: Object,
  },
});

const frequentTermsObject = [
  {
    term: 'normal',
    style: {'color': 'var(--rosalution-purple-300)'},
    icon: '',
    iconStyle: {},
  },
  {
    term: 'abnormal',
    style: {'color': 'var(--rosalution-red-100)'},
    icon: '',
    iconStyle: {},
  },
  {
    term: 'absent',
    style: {'color': 'var(--rosalution-red-100)'},
    icon: '',
    iconStyle: {},
  },
  {
    term: 'increased',
    style: {'color': 'var(--rosalution-purple-300)'},
    icon: 'arrow-up',
    iconStyle: {'color': 'purple'},
  },
  {
    term: 'decreased',
    style: {'color': 'var(--rosalution-red-100)'},
    icon: 'arrow-down',
    iconStyle: {'color': 'var(--rosalution-red-100)'},
  },
];

const animalModel =  chooseAnimalModelsSchema(props.model);

function calculateAssociatedPhenotypes() {
  const phenotypesDict = {'':
        {
          phenotypes: [],
          style: '',
          icon: '',
          iconStyle: {},
        },
  };

  if ( 'phenotypes' in animalModel == false) {
    return phenotypesDict;
  }

  animalModel.phenotypes.forEach((phenotype) => {
    phenotypesDict[''].phenotypes.push(phenotype);
  });

  frequentTermsObject.forEach((term) => {
    phenotypesDict[term.term] = {
      phenotypes: [],
      style: term.style,
      icon: term.icon,
      iconStyle: term.iconStyle,
    };
  });

  animalModel.phenotypes.forEach((phenotype) => {
    frequentTermsObject.forEach((term) => {
      const regex = new RegExp('\\b' + term.term + '\\b', 'i');

      if (phenotype.match(regex)) {
        phenotypesDict[term.term].phenotypes.push(phenotype);
        phenotypesDict[''].phenotypes.splice(phenotypesDict[''].phenotypes.indexOf(phenotype), 1);
      }
    });
  });

  Object.keys(phenotypesDict).forEach((key) => {
    if (!phenotypesDict[key].phenotypes.length) {
      delete phenotypesDict[key];
    }
  });

  return phenotypesDict;
};

const modelName = computed(()=> {
  const regex = new RegExp('^(.*?)(?= \\[)', 'g');
  if ('name' in animalModel == false) {
    return '';
  }
  console.log(animalModel);
  const matchResult = animalModel.name.match(regex);

  if (matchResult) {
    return matchResult[0];
  }

  return animalModel.name;
});

const modelBackground = computed(() => {
  // This escape character is very necessary, but eslint doesn't think so
  const regex = new RegExp(`\\[background:\]?(.*)`, 'g'); // eslint-disable-line

  if ('background' in animalModel == false) {
    return '';
  }

  const matchResult = animalModel.background.match(regex);

  if (matchResult) {
    return matchResult[0];
  }

  return '';
});

const modelSource = computed(() => {
  if ( 'source' in animalModel == false ) {
    return '';
  }
  return animalModel['source'];
});

const associatedPhenotypesData = calculateAssociatedPhenotypes();
const experimentalConditions = 'conditions' in animalModel ? animalModel.conditions : [];
const diseaseModels = 'diseaseModels' in animalModel ? animalModel.diseaseModels: [];


function sectionTextColor(section) {
  console.log(section);
  console.log('inside the text color calcdulation');

  const hasEmptyContent =
    section === undefined ||
    section === null ||
    Object.keys(section).length === 0 ||
    section.length === 0;
  const hasPhenotypeContentButItsEmpty = Object.keys(section).length === 1 && section?.['']?.phenotypes.length ===0;

  if ( hasEmptyContent || hasPhenotypeContentButItsEmpty ) {
    return {color: `var(--rosalution-grey-300)`};
  }

  return 'color: black';
};
</script>

<style scoped>
ul {
  list-style-type: disc;
  padding-left: 7%;
}

li {
  margin-left: var(--p-10);
  padding-top: 1%;
  font-size: 15px;
}

.card-header {
    font-size: 22px;
    font-weight: bold;
}

.card-sub-header {
    font-size: 16px;
    padding-top: 2%;
}

.card-base {
  text-decoration: none;
  width: 30rem;
  padding: var(--p-8);
  background-color: var(--rosalution-grey-50);
  box-sizing: border-box;
  color: inherit;
  border-radius: var(--content-border-radius);
  height: 35rem;
  overflow-y: scroll;
}

.card-content {
    padding-bottom: 10%;
}

.card-section {
    font-weight: bold;
    padding-top: 2.5%;
}

.card-section-term {
    padding-left: var(--p-5);
}

.card-list {
    padding-top: 1%;
    padding-left: 5%;
    font-size: 16px;
}

.card-source {
  padding-top: 2%;
}

</style>
