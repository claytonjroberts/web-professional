

<template>
<div :class="'col-auto border skill '+ (skilldict.use ? 'hoverable ' : '') + ($parent.skilladditional == skillkey ? 'hover': '')"
     @click="$parent.skilladditional = ($parent.skilladditional == skillkey ? null : skillkey)"
     @mouseover="showlink = true"
     @mouseleave="showlink=false">


    <div class="row d-flex justify-content-between">
        <!-- <div class="col-2 d-flex text-muted" style="text-align: center; justify-content:center;"> -->
        <div class="col"
             v-if="showIcon">
            <h4>
                <i :class="skilldict.icon ? skilldict.icon : parentDict.icon"
                   style="align-self:center;"></i>
            </h4>
        </div>
        <div class="col"
             v-if="showIconText">
            <h4>
                {{ skilldict.icontext }}
            </h4>
        </div>
        <div class="col-auto px-1">
            {{ skillkey }} <span v-if="skilldict.parent">(<span class="skill-text-parent">{{ skilldict["parent"] }}</span>)</span>
        </div>
        <div class="col">
            <div class="text-tertiary stars">
                <i class="fas fa-star fa-xs"
                   v-for="x in this.$_.range(Math.ceil(skilldict.level/2))"
                   :key="`star-${x}`">
                </i><i class="far fa-star fa-xs"
                   v-for="x in this.$_.range(3 - Math.ceil(skilldict.level/2))"
                   :key="`star-empty-${x}`">
                </i>
            </div>
        </div>
    </div>

    <!-- <div class="row">

        <div class="col-auto px-1">
            {{ skillkey }}
        </div>
        <div class="col-auto px-1"
             v-if="skilldict.parent">
            (<span class="text-muted">{{ skilldict["parent"] }}</span>)
        </div>

    </div> -->

    <div class="row"
         v-if="($parent.skilladditional == skillkey) && (skilldict.use)">
        <p class="px-1 text-muted">
            {{ skilldict.use }}
        </p>
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
    data: function () {
        return {
            showadditional: false,
            showlink: false,
        }
    },
    computed: {
        doshow() {
            return true;
            // `this` points to the vm instance
            var self = this;

            if (this.$parent.filterexperience) {
                return (0 <= _.indexOf(this.$parent.filterexperience, self.skillkey))
            }
            // return true;
            else if (this.$parent.filtersearch) {
                return (self.skillkey.includes(self.$parent.filtersearch) || (self.skilldict.parent && self.skilldict.parent.includes(self.$parent.filtersearch)));
            } else {
                return true;
            }

        },
        showIcon() {
            return (
                this.skilldict.icon || (this.parentDict && this.parentDict.icon)
            )
        },
        showIconText() {
            return (
                !(this.showIcon) &&
                (
                    this.skilldict.icontext ||
                    (this.parentDict && this.parentDict.icon)
                )
            )
        },
        parentDict() {
            var self = this;

            if (self.skilldict.parent) {
                return this.$parent.info.skills.list[self.skilldict.parent];
            } else {
                return null;
            }
        },
        stars: function () {
            var self = this;

            return _.range(Math.ceil(this.skilldict.level / 2))
        }

    },
    methods: {
        from_markdown_to_html: function (x) {
            return mdconverter.makeHtml(x);
        },
        sort_experience: function (x) {

        }
    },
}
</script>
