import React from 'react';
import Typography from '@material-ui/core/Typography';

import SpellList from './components/spell_list';
import SpellForm from './components/spell_form';
import SpellsData from './data/spells.json';

import './App.css';



class SpellApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      spells: SpellsData,
      spells_curr: SpellsData
    }
  }

  filter(name) {
    if (name.length >= 3) {
      this.setState({
        spells_curr:
          this.state.spells.filter((spell) => {
            return spell.Name.toLowerCase().includes(name)
          })
      });
    }
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <Typography variant="h2" component="h2">
            Spell Slinger
          </Typography>
        </header>

        <SpellForm updateSpell={this.filter.bind(this)} />

        <div className="App-spells">
          <br />
          <br />
          <SpellList spells={this.state.spells_curr} />
        </div>
      </div>
    );
  }
}

export default SpellApp;