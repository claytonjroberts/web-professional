

<template>
<div class="col-auto border skill"
     @click="$parent.skilladditional = ($parent.skilladditional == skillkey ? null : skillkey)"
     @mouseover="showlink = true"
     @mouseleave="showlink=false">


    <div class="row justify-content-start">
        <div class="col-1 skill-stars" style="text-align: center;">
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
        <div class="col-1 skill-icon" style="min-width: 3em; text-align: center;">
            <h4 v-if="showIcon">
                <i :class="skilldict.icon ? skilldict.icon : parentDict.icon"
                   style="align-self:center;"></i>
            </h4>
            <h4 v-if="showIconText">
                {{ skilldict.icontext }}
            </h4>
        </div>
        <div class="col-4 px-1 skill-name">
            {{ skillkey }} <span v-if="skilldict.parent">(<span class="skill-text-parent">{{ skilldict["parent"] }}</span>)</span>
        </div>
        <div class="col-6 skill-description">
            <span class="text-muted">
                {{ skilldict.use }}
            </span>
        </div>
    </div>
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
