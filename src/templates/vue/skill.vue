

<template>
<div :class="'col-auto border skill '+ (skilldict.use ? 'hoverable ' : '') + ($parent.skilladditional == skillkey ? 'hover': '')" v-if="doShow" @click="$parent.skilladditional = skillkey" @mouseover="showlink = true" @mouseleave="showlink=false">


    <div class="row d-flex justify-content-between text-muted">
        <!-- <div class="col-2 d-flex text-muted" style="text-align: center; justify-content:center;"> -->
        <h4 v-if="(skilldict.icon || (parentDict && parentDict.icon))">
            <i :class="skilldict.icon ? skilldict.icon : parentDict.icon" style="align-self:center;"></i>
        </h4>
        <h4 v-else-if="(skilldict.icontext || (parentDict && parentDict.icon))">
            {{ skilldict.icontext }}
        </h4>

        <div class="text-tertiary stars">
            <!-- v-if="!showlink || !skilldict.link" -->
            <i class="far fa-star fa-xs" v-for="x in this.$_.range(3 - Math.ceil(skilldict.level/2))">
            </i><i class="fas fa-star fa-xs" v-for="x in this.$_.range(Math.ceil(skilldict.level/2))">
            </i>
        </div>

    </div>

    <div class="row">

        <div class="col-auto px-1">
            {{ skillkey }}
        </div>
        <div class="col-auto px-1" v-if="skilldict.parent">
            (<span class="text-muted">{{ skilldict["parent"] }}</span>)
        </div>

    </div>
    <!-- </div> -->
    <!-- <div class="col-8 d-flex flex-wrap pl-0">
            <div class="center-vertical">

            </div>


        </div> -->


    <!-- <div class="col-2">

            <div class="text-tertiary stars" v-if="!showlink || !skilldict.link">
                <i class="far fa-star fa-xs" v-for="x in this.$_.range(3 - Math.ceil(skilldict.level/2))">
                </i><i class="fas fa-star fa-xs" v-for="x in this.$_.range(Math.ceil(skilldict.level/2))">
                </i>
            </div>

            <a v-if="showlink && skilldict.link" class="center-vertical" style="text-align:center;" :href="skilldict.link">
                <i class="fas fa-external-link-alt"></i>
            </a>

        </div>
        <div class="row pt-2 p-1" v-if="($parent.skilladditional == skillkey) && (skilldict.use)">
            <div class="col">
                <p class="p-1 mb-0">
                    {{ skilldict.use }}
                </p>
            </div>



        </div> -->



</div>
</template>


<script>
export default {
    name: "skill",
    props: [
        "skilldict",
        "skillkey",
    ],
    data: function() {
        return {
            showadditional: false,
            showlink: false,
        }
    },
    computed: {
        doShow: function() {
            // `this` points to the vm instance
            var self = this;

            if (this.$parent.filterexperiance) {
                return (0 <= _.indexOf(this.$parent.filterexperiance, self.skillkey))
            }
            // return true;
            else if (this.$parent.filtersearch) {
                return (self.skillkey.includes(self.$parent.filtersearch) || (self.skilldict.parent && self.skilldict.parent.includes(self.$parent.filtersearch)));
            } else {
                return true;
            }

        },
        parentDict: function() {
            var self = this;

            if (self.skilldict.parent) {
                return this.$parent.info.skills.list[self.skilldict.parent];
            } else {
                return null;
            }
        },
        stars: function() {
            var self = this;

            return _.range(Math.ceil(this.skilldict.level / 2))
        }

    },
    methods: {
        from_markdown_to_html: function(x) {
            return mdconverter.makeHtml(x);
        },
        sort_experience: function(x) {

        }
    },
}
</script>
