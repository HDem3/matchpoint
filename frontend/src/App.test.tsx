import {render,screen} from '@testing-library/react'; import {vi} from 'vitest'; import {App} from './App';
vi.stubGlobal('fetch',vi.fn(()=>Promise.resolve({json:()=>Promise.resolve([])})));
test('renders product name',()=>{render(<App/>);expect(screen.getByText('MatchPoint')).toBeInTheDocument()});


